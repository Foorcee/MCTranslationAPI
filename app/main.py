from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
from .model import translate, TranslationResponse, TranslationRequest

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/translate/{source}-{target}", name="Translates a text", response_model=TranslationResponse)
async def translate_request(source: str, target: str, body: Annotated[TranslationRequest, Form()]):
    return translate(source, target, body.text)
