from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import HTTPException
from pydantic import BaseModel
import os
import timeit
import torch

MODEL_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'model')
model = AutoModelForSeq2SeqLM.from_pretrained('Foorcee/t5-minecraft-de-en-base', cache_dir=MODEL_CACHE_DIR)
tokenizer = AutoTokenizer.from_pretrained('Foorcee/t5-minecraft-de-en-base', cache_dir=MODEL_CACHE_DIR)

MAX_LEN = 256

LANG_MAPPING = {
    "de": "German",
    "en": "English"
}

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    input: str
    output: str
    token: int
    time: float

def map_language(lang, name):
    if lang is None:
        raise HTTPException(status_code=400, detail=f"Invalid {name} language")

    if lang in LANG_MAPPING:
        return LANG_MAPPING[lang]
    else:
        raise HTTPException(status_code=400, detail=f"Invalid {name} language")

def _substitute_unk_token(input_text, output_ids, unk_in_idx, unk_out_idx):
    input_tokens = tokenizer.tokenize(input_text)

    decoded_tokens = tokenizer.convert_ids_to_tokens(output_ids)

    for idx in range(len(unk_out_idx)):
        if  idx < len(unk_in_idx):
            decoded_tokens[unk_out_idx[idx]] = input_tokens[unk_in_idx[idx]]

    return tokenizer.convert_tokens_to_string(decoded_tokens[1:-1])


def _decode_output(input_text, input_ids, output_ids):
    unk_out_idx = torch.nonzero(output_ids == tokenizer.unk_token_id)
    if len(unk_out_idx) > 0:
        unk_in_idx = torch.nonzero(input_ids == tokenizer.unk_token_id)
        return _substitute_unk_token(input_text, output_ids, unk_in_idx, unk_out_idx)
    else:
        return tokenizer.decode(output_ids, skip_special_tokens=True)


def translate(source_lang, target_lang, text):
    start_time = timeit.default_timer()

    in_lang = map_language(source_lang, "source")
    out_lang = map_language(target_lang, "target")

    if in_lang == out_lang:
        raise HTTPException(status_code=400, detail=f"Language {in_lang} and language {out_lang} are equal")

    input_texts = [f'translate {in_lang} to {out_lang}: {text}']

    # Tokenize the input texts
    input_tokenized = tokenizer(input_texts, max_length=MAX_LEN, padding=True, truncation=True, return_tensors='pt')

    input_ids = input_tokenized['input_ids']

    # Generate the output
    outputs = model.generate(input_ids=input_ids, attention_mask=input_tokenized["attention_mask"], max_length=MAX_LEN)

    output_text = _decode_output(input_texts[0], input_ids[0], outputs[0])

    end_time = timeit.default_timer()
    elapsed_time_ms = (end_time - start_time) * 1000

    return TranslationResponse(input=text, output=output_text, token=len(input_ids[0]), time=elapsed_time_ms)

