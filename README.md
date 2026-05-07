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
- UI for interaction

---

## Tech used

- Python 3
- FastAPI
- langdetect
- faster-whisper
- HTML / JavaScript
- pytest
- requests

---

## How to run

```bash
conda activate swp-project
uvicorn app.main:app --reload 
```

Open in browser 
[API docs](http://127.0.0.1:8000/docs)

To access the UI:
```bash
open ui/index.html
```

---

## Running Tests

### Unit Tests
```bash
python -m pytest
```

### Coverage Report
```bash
python -m pytest --cov=app
```

### Coverage Report with HTML Output
```bash
python -m pytest --cov=app --cov-report=html
```

### Other Tests
```bash
python tests/test_requests.py
```

## API Endpoints
- GET /health
- GET /supported-languages
- POST /detect-language/text
- POST /detect-language/voice
- POST /dialog/respond
- POST /detect-code-switching

