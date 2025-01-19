# REST API for T5-Minecraft-DE-EN Model

This project provides a REST API built using Python's FastAPI framework to load and query the t5-minecraft-de-en-base model. 
This model is fine-tuned for translating styled Minecraft messages between German and English, supporting legacy color codes and MiniMessage format.

Modelcard: [Foorcee/t5-minecraft-de-en-base](https://huggingface.co/Foorcee/t5-minecraft-de-en-base)

## API Endpoints

1. `POST /translate/de-en`
2. `POST /translate/en-de`

Example Request (cURL):
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/translate/de-en' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'text=%3Cgray%3EDer%20Befehl%20wurde%20%3Cgreen%3Eerfolgreich%20%3Cgray%3Eausgef%C3%BChrt.'
```

Example Response:
```json
{
  "input": "<gray>Der Befehl wurde <green>erfolgreich <gray>ausgeführt.",
  "output": "<gray>The command was <green>successfully <gray>executed.",
  "token": 30,
  "time": 363.25141699998653
}
```

## Features:
 - Back Replacement from Unk Token: All unknown tokens (UNK) will be extracted from the source string and reinserted into the translated string. Typical UNK tokens include Unicode characters.

