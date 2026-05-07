# Language Detection Dialog System

## Wprowadzenie

**Language Detection Dialog System** to prosty system do identyfikacji języka (LID) w wielojęzycznych dialogach. System automatycznie wykrywa język danych wejściowych użytkownika, obsługuje podstawowe odpowiedzi dialogowe i identyfikuje code-switching (zmianę kodu) między wypowiedziami.

## Główne cechy

- 🔍 **Detekcja języka** - automatyczne rozpoznawanie języka tekstu
- 🗣️ **Wsparcie dla głosu** - rozpoznawanie mowy + detekcja języka + analiza code-switching
- 💬 **Dialog** - podstawowe odpowiedzi dostosowane do wykrytego języka
- 🔀 **Detekcja code-switching** - identyfikacja zmiany języka między wypowiedziami
- 📱 **Interfejs użytkownika** - prosty UI do interakcji z systemem
- ✅ **System health check** - sprawdzenie stanu systemu
- 📊 **Lista obsługiwanych języków** - informacje o dostępnych językach

## Technologia

| Narzędzie | Opis |
|-----------|------|
| **Python 3** | Język programowania |
| **FastAPI** | Framework do budowy API |
| **langdetect** | Biblioteka do detekcji języka |
| **faster-whisper** | Model do rozpoznawania mowy (ASR) |
| **pytest** | Framework do testowania |
| **HTML/JavaScript** | Frontend aplikacji |

## Szybki start

### Wymagania
- Python 3.8+
- Conda lub pip

### Instalacja i uruchomienie

```bash
# Aktywuj środowisko Conda
conda activate swp-project

# Uruchom serwer API
uvicorn app.main:app --reload
```

API będzie dostępne pod adresem `http://127.0.0.1:8000`

### Dokumentacja API

Po uruchomieniu serwera możesz zapoznać się z dokumentacją interaktywną:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Interfejs użytkownika

Aby otworzyć interfejs użytkownika:

```bash
open ui/index.html
```

## Testy

Projekt zawiera kompleksowe testy:

```bash
# Uruchom wszystkie testy
python -m pytest

# Pokrycie kodu
python -m pytest --cov=app

# Raport pokrycia w HTML
python -m pytest --cov=app --cov-report=html
```

## Struktura projektu

```
.
├── app/                      # Kod aplikacji
│   ├── main.py              # Główna aplikacja FastAPI
│   ├── service.py           # Logika detekcji języka i dialogu
│   └── asr_service.py       # Rozpoznawanie mowy
├── tests/                    # Testy jednostkowe
├── ui/                       # Interfejs użytkownika
│   └── index.html           # HTML UI
├── docs/                     # Dokumentacja (ten folder)
├── requirements.txt          # Zależności Python
├── pytest.ini               # Konfiguracja pytest
├── openapi.yaml             # Specyfikacja OpenAPI
└── docker-compose.yml       # Konfiguracja Docker
```

## Dokumentacja

W tym projekcie możesz znaleźć:

- [Getting Started](getting-started.md) - Szczegółowy przewodnik po начинaniu pracy
- [API Reference](api.md) - Pełna dokumentacja endpointów API
- [Funkcje](features.md) - Opis wszystkich funkcji
- [Development](development.md) - Przewodnik dla programistów
- [Deployment](deployment.md) - Wdrażanie i Docker

## Kontakt i wsparcie

Aby uzyskać więcej informacji, zapoznaj się z [README.md](../README.md) w głównym folderze projektu.
