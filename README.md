# Language Detection Dialog System

Simple system for language identification (LID) in multilingual dialogue.

The project detects the language of user input, handles basic dialog responses, and identifies code-switching between utterances.

---

## Features

- Language detection (text)
- Simple dialog response based on detected language
- Code-switching detection (between utterances - text)
- List of supported languages
- Basic system health check
- Voice input support (ASR + LID + code-switching)
- (Planned) UI for interaction

---

## Tech used

- Python 3
- FastAPI
- langdetect

---

## How to run

```bash
conda activate swp-project
uvicorn app.main:app --reload 
```

Open in browser 
[API docs](http://127.0.0.1:8000/docs)

---

## API Endpoints
- GET /health
- GET /supported-languages
- POST /detect-language/text
- POST /detect-language/voice
- POST /dialog/respond
- POST /detect-code-switching

