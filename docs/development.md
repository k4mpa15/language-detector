# Development Guide

## Dla programistów

Przewodnik do rozwijania i rozszerzania Language Detection Dialog System.

## Struktura kodu

```
app/
├── main.py           # Główna aplikacja FastAPI, definicje routes
├── service.py        # Logika biznesowa - detekcja języka, dialog, code-switching
└── asr_service.py    # Obsługa rozpoznawania mowy (ASR)

tests/
├── test_main.py      # Testy routes/endpointów
├── test_service.py   # Testy logiki biznesowej
├── test_asr_service.py   # Testy ASR
└── test_requests.py  # Testy integracyjne
```

## Setup środowiska developmentu

### 1. Klonowanie i instalacja

```bash
git clone <repo-url>
cd systemy_dialogowe_projekt
conda create -n swp-project python=3.10
conda activate swp-project
pip install -r requirements.txt
```

### 2. Instalacja dev zależności (opcjonalnie)

```bash
pip install black flake8 mypy
```

## Uruchomienie w trybie developmentu

```bash
conda activate swp-project
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Flaga `--reload` automatycznie restartuje serwer przy zmianach kodu.

## Testowanie

### Uruchomienie testów

```bash
# Wszystkie testy
python -m pytest

# Testy z verbose output
python -m pytest -v

# Testy konkretnego pliku
python -m pytest tests/test_service.py

# Testy konkretnej funkcji
python -m pytest tests/test_service.py::test_detect_language_english
```

### Pokrycie kodu

```bash
# Raport w terminalu
python -m pytest --cov=app

# Raport HTML
python -m pytest --cov=app --cov-report=html
# Otwórz: htmlcov/index.html
```

### Testowanie manualne

Używając Swagger UI:
```
http://127.0.0.1:8000/docs
```

Lub cURL:
```bash
curl -X POST http://127.0.0.1:8000/detect-language/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

## Główne komponenty

### 1. Detekcja języka (`app/service.py`)

```python
def detect_language(text: str) -> dict:
    """Detects language from text."""
    detected = detect(text)
    confidence = detect_langs(text)[0].prob
    language_name = LANGUAGE_MAP.get(detected, detected)
    return {
        "language": detected,
        "language_name": language_name,
        "confidence": confidence
    }
```

Używa biblioteki `langdetect`.

### 2. ASR - Rozpoznawanie mowy (`app/asr_service.py`)

```python
def transcribe_audio_with_segments(audio_path: str) -> dict:
    """Transcribes audio and detects language."""
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path)
    # Zwraca transkrypcję, język, confidence
```

Używa `faster-whisper` (szybsza implementacja OpenAI Whisper).

### 3. Endpointy API (`app/main.py`)

```python
@app.post("/detect-language/text")
async def detect_language_text(request: Request):
    """Endpoint do detekcji języka z tekstu."""
    data = await request.json()
    text = data.get("text", "").strip()
    return detect_language(text)
```

## Dodawanie nowych funkcji

### Przykład: Dodanie nowego endpointu

1. **Dodaj funkcję w `app/service.py`**:

```python
def my_new_feature(input_text: str) -> dict:
    """Moja nowa funkcja."""
    # Logika tutaj
    return {"result": "value"}
```

2. **Dodaj endpoint w `app/main.py`**:

```python
@app.post("/my-new-endpoint")
async def my_new_endpoint(request: Request):
    """Dokumentacja endpointu."""
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        if not text:
            return {"error": "Pole 'text' jest wymagane"}
        result = my_new_feature(text)
        return result
    except Exception as e:
        return {"error": str(e)}
```

3. **Dodaj testy w `tests/test_service.py` lub `tests/test_main.py`**:

```python
def test_my_new_feature():
    result = my_new_feature("test input")
    assert result["result"] == "expected_value"
```

4. **Uruchom testy**:

```bash
python -m pytest tests/test_main.py::test_my_new_endpoint -v
```

## Dodawanie nowych języków

Języki są obsługiwane automatycznie przez `langdetect`. Jednak jeśli chcesz dodać obsługę dla konkretnego języka w dialogu:

1. **Zaktualizuj `LANGUAGE_MAP` w `app/service.py`**:

```python
LANGUAGE_MAP = {
    'en': 'English',
    'pl': 'Polish',
    'fr': 'French',  # Nowy język
    # ...
}
```

2. **Dodaj odpowiedzi dialogowe dla nowego języka**:

```python
DIALOG_RESPONSES = {
    'en': {'greeting': 'Hello! How can I help you?', ...},
    'pl': {'greeting': 'Cześć! Jak się masz?', ...},
    'fr': {'greeting': 'Bonjour! Comment puis-je vous aider?', ...},  # Nowy
    # ...
}
```

3. **Testy**:

```bash
python -m pytest tests/test_service.py -v
```

## Code Style

Projekt używa:
- **Black** - formatowanie kodu
- **Flake8** - linting
- **Type hints** - adnotacje typów

### Formatowanie kodu

```bash
black app/ tests/
```

### Linting

```bash
flake8 app/ tests/
```

### Type checking

```bash
mypy app/
```

## Debugowanie

### Logowanie

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Processing text: {text}")
logger.debug(f"Detected language: {detected}")
logger.error(f"Error occurred: {e}")
```

### Debugger - VSCode

1. Dodaj breakpoint w kodzie (kliknij obok numeru linii)
2. Uruchom `python -m pdb app/main.py`
3. Lub użyj VSCode debugger (F5)

### Debug endpoint w Swagger UI

```
http://127.0.0.1:8000/docs
```

## Optymalizacja

### Performance profiling

```bash
python -m cProfile -s cumulative app/main.py
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def detect_language_cached(text: str) -> dict:
    return detect_language(text)
```

## CI/CD

Projekt może być zintegrowany z GitHub Actions, GitLab CI, itp.

### Przykład GitHub Actions workflow

```yaml
name: Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
```

## Przydatne linki

- [FastAPI dokumentacja](https://fastapi.tiangolo.com/)
- [langdetect GitHub](https://github.com/Mimino666/langdetect)
- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [pytest dokumentacja](https://docs.pytest.org/)

## Troubleshooting

### Problem: Import errors

```bash
pip install -r requirements.txt
```

### Problem: Model nie ładuje się

```python
# Wymuś pobranie modelu
from faster_whisper import WhisperModel
model = WhisperModel("base")
```

### Problem: Testy nie działają

```bash
# Sprawdź czy pytest jest zainstalowany
pip install pytest pytest-cov

# Uruchom z verbose
pytest -vv
```

## Kontrybuowanie

1. Utwórz branch: `git checkout -b feature/my-feature`
2. Commit zmiany: `git commit -am 'Add new feature'`
3. Push: `git push origin feature/my-feature`
4. Otwórz Pull Request

Upewnij się że:
- Wszystkie testy przechodzą
- Kod jest sformatowany (black)
- Brak linting errors (flake8)
