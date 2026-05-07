# Getting Started

## Wymagania systemowe

- **Python**: 3.8 lub nowszy
- **Conda** (rekomendowane) lub pip
- **Git** (do klonowania repozytorium)
- ~2GB RAM (dla modelów NLP)

## Instalacja

### Krok 1: Klonowanie repozytorium

```bash
git clone <repository-url>
cd systemy_dialogowe_projekt
```

### Krok 2: Tworzenie środowiska Conda

```bash
conda create -n swp-project python=3.10
conda activate swp-project
```

### Krok 3: Instalacja zależności

```bash
pip install -r requirements.txt
```

## Uruchomienie aplikacji

### Tryb development

```bash
conda activate swp-project
uvicorn app.main:app --reload
```

Serwer uruchomi się pod adresem: **http://127.0.0.1:8000**

Możesz otrzymać taki komunikat:
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Sprawdzenie, czy aplikacja działa

Otwórz przeglądarkę i przejdź do:

```
http://127.0.0.1:8000/health
```

Powinieneś zobaczyć:
```json
{"status": "ok"}
```

## Korzystanie z API

### Via cURL

Detekcja języka z tekstu:

```bash
curl -X POST "http://127.0.0.1:8000/detect-language/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

Odpowiedź:
```json
{
  "language": "en",
  "language_name": "English",
  "confidence": 0.95
}
```

### Via Swagger UI

Otwórz stronę dokumentacji:

```
http://127.0.0.1:8000/docs
```

Tutaj możesz testować wszystkie endpointy interaktywnie.

## Korzystanie z interfejsu użytkownika

### Otwarcie UI

```bash
open ui/index.html
```

Interfejs pozwala na:
- Wpisywanie tekstu i detekcję języka
- Nagrywanie mowy i jej analizę
- Przeglądanie wyników detekcji
- Testowanie code-switching detection

## Pierwsze kroki z kodem

### Struktura katalogów

```
app/
├── main.py           # Punkty wejścia API (routes)
├── service.py        # Logika biznesowa
└── asr_service.py    # Obsługa audio
```

### Przykładowe użycie w kodzie Python

```python
from app.service import detect_language, LANGUAGE_MAP

# Detekcja języka
result = detect_language("Cześć, jak się masz?")
print(result)
# Output: {'language': 'pl', 'language_name': 'Polish', 'confidence': 0.98}

# Lista obsługiwanych języków
print(LANGUAGE_MAP)
```

## Troubleshooting

### Problem: Port 8000 już w użyciu

```bash
# Użyj innego portu
uvicorn app.main:app --reload --port 8001
```

### Problem: Błąd przy importowaniu torch

```bash
# Zainstaluj torch ręcznie
pip install torch torchvision torchaudio
```

### Problem: Brak modelu whisper

```bash
# Model będzie pobrany automatycznie przy pierwszym użyciu
# Jeśli masz problemy, możesz go pobrać ręcznie:
from faster_whisper import WhisperModel
model = WhisperModel("base")
```

## Następne kroki

- Przeczytaj [API Reference](api.md) aby poznać wszystkie dostępne endpointy
- Sprawdź [Features](features.md) aby dowiedzieć się o wszystkich możliwościach
- Dla developerów: [Development Guide](development.md)
- Informacje o deploymencie: [Deployment](deployment.md)
