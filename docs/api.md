# API Reference

## Przegląd

API Language Detection Dialog System udostępnia endpointy do:
- Detekcji języka z tekstu i mowy
- Odpowiadania na wiadomości w dialogu
- Detekcji code-switching
- Pobrania listy obsługiwanych języków
- Sprawdzenia stanu systemu

**Base URL**: `http://127.0.0.1:8000`

## Endpointy

### Health Check

#### `GET /health`

Sprawdza, czy system jest uruchomiony i gotowy do pracy.

**Żadnych parametrów**

**Odpowiedź (200 OK)**:
```json
{
  "status": "ok"
}
```

**Przykład**:
```bash
curl http://127.0.0.1:8000/health
```

---

### Obsługiwane języki

#### `GET /supported-languages`

Zwraca listę wszystkich obsługiwanych języków.

**Żadnych parametrów**

**Odpowiedź (200 OK)**:
```json
{
  "supported_languages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "pl",
      "name": "Polish"
    },
    {
      "code": "es",
      "name": "Spanish"
    },
    ...
  ]
}
```

**Przykład**:
```bash
curl http://127.0.0.1:8000/supported-languages
```

---

### Detekcja języka z tekstu

#### `POST /detect-language/text`

Wykrywa język podanego tekstu.

**Request Body**:
```json
{
  "text": "Hello world"
}
```

**Parametry**:
- `text` (string, wymagane) - Tekst do analizy

**Odpowiedź (200 OK)**:
```json
{
  "language": "en",
  "language_name": "English",
  "confidence": 0.95
}
```

**Parametry odpowiedzi**:
- `language` (string) - Kod języka ISO 639-1
- `language_name` (string) - Pełna nazwa języka
- `confidence` (number) - Pewność detekcji (0-1)

**Przykłady**:

```bash
# Angielski
curl -X POST http://127.0.0.1:8000/detect-language/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

# Polski
curl -X POST http://127.0.0.1:8000/detect-language/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Cześć, jak się masz?"}'

# Hiszpański
curl -X POST http://127.0.0.1:8000/detect-language/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola mundo"}'
```

---

### Detekcja języka z mowy (audio)

#### `POST /detect-language/voice`

Transkrybuje audio, wykrywa język i identyfikuje code-switching.

**Request Body**: `multipart/form-data`
- `file` (file, wymagane) - Plik audio (format: WAV, MP3, OGG, FLAC, itp.)

**Odpowiedź (200 OK)**:
```json
{
  "transcription": "Hello world",
  "language": "en",
  "language_name": "English",
  "confidence": 0.92,
  "code_switching_detected": false
}
```

**Parametry odpowiedzi**:
- `transcription` (string) - Transkrypcja tekstu z audio
- `language` (string) - Kod wykrytego języka
- `language_name` (string) - Pełna nazwa języka
- `confidence` (number) - Pewność detekcji (0-1)
- `code_switching_detected` (boolean) - Czy wykryto zmianę języka

**Przykład** (Python):
```python
import requests

with open("audio.wav", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://127.0.0.1:8000/detect-language/voice",
        files=files
    )
    print(response.json())
```

**Przykład** (cURL):
```bash
curl -X POST http://127.0.0.1:8000/detect-language/voice \
  -F "file=@audio.wav"
```

---

### Dialog - Odpowiedź

#### `POST /dialog/respond`

Udziela odpowiedzi dialogowej na podstawie tekstu wejściowego. Odpowiedź dostosowana jest do wykrytego języka.

**Request Body**:
```json
{
  "text": "Hello"
}
```

**Parametry**:
- `text` (string, wymagane) - Tekst użytkownika

**Odpowiedź (200 OK)**:
```json
{
  "response": "Hello! How can I help you?",
  "language": "en",
  "language_name": "English"
}
```

**Parametry odpowiedzi**:
- `response` (string) - Odpowiedź systemu dostosowana do języka
- `language` (string) - Kod wykrytego języka
- `language_name` (string) - Pełna nazwa języka

**Przykłady**:

```bash
# Angielski
curl -X POST http://127.0.0.1:8000/dialog/respond \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello"}'

# Polski
curl -X POST http://127.0.0.1:8000/dialog/respond \
  -H "Content-Type: application/json" \
  -d '{"text": "Cześć"}'
```

---

### Detekcja Code-Switching

#### `POST /detect-code-switching`

Identyfikuje czy w tekście doszło do zmiany języka (code-switching) między poszczególnymi fragmentami lub wypowiedziami.

**Request Body**:
```json
{
  "text": "Hello, jak się masz? Good morning"
}
```

**Parametry**:
- `text` (string, wymagane) - Tekst do analizy

**Odpowiedź (200 OK)**:
```json
{
  "code_switching_detected": true,
  "languages_detected": ["en", "pl"],
  "segments": [
    {
      "text": "Hello",
      "language": "en",
      "language_name": "English"
    },
    {
      "text": "jak się masz",
      "language": "pl",
      "language_name": "Polish"
    },
    {
      "text": "Good morning",
      "language": "en",
      "language_name": "English"
    }
  ]
}
```

**Parametry odpowiedzi**:
- `code_switching_detected` (boolean) - Czy wykryto zmianę języka
- `languages_detected` (array) - Lista kodów języków użytych w tekście
- `segments` (array) - Szczegóły dla każdego segmentu tekstu
  - `text` - Fragment tekstu
  - `language` - Kod języka
  - `language_name` - Pełna nazwa języka

**Przykład**:
```bash
curl -X POST http://127.0.0.1:8000/detect-code-switching \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, jak się masz? Good morning"}'
```

---

## Kody błędów

### 400 Bad Request

Zwracany gdy request jest niepoprawny.

```json
{
  "error": "Pole 'text' jest wymagane"
}
```

### 422 Unprocessable Entity

Zwracany gdy parametry Request Body nie pasują do schematu.

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "text"],
      "msg": "Field required"
    }
  ]
}
```

### 500 Internal Server Error

Zwracany gdy na serwerze dojdzie do błędu.

```json
{
  "error": "Wewnętrzny błąd serwera"
}
```

---

## Interaktywna dokumentacja

Po uruchomieniu aplikacji możesz zapoznać się z interaktywną dokumentacją:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Tam możesz testować endpointy bezpośrednio w przeglądarce!

---

## Limity

Nie ma zdefiniowanych limitów rate-limiting na ten moment. Aplikacja przyjmuje:
- Maksymalny rozmiar tekstu: nie ograniczony
- Maksymalny rozmiar pliku audio: do 50MB (zależy od konfiguracji)

## CORS

API ma włączony CORS dla wszystkich źródeł (`*`), co pozwala na wywoływanie API z dowolnej domeny.
