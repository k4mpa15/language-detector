# Funkcje

## Przegląd funkcji

System Language Detection Dialog oferuje kilka głównych funkcji do pracy z wielojęzycznym dialogiem:

## 1. Detekcja języka z tekstu 🔍

Automatyczne wykrycie języka tekstu wejściowego.

**Jak to działa**:
- System analizuje podany tekst
- Wykorzystuje bibliotekę `langdetect` do identyfikacji języka
- Zwraca kod języka (np. "en", "pl", "es") oraz pewność detekcji

**Obsługiwane języki**: ~55 języków (z biblioteki langdetect)

**Przykład**:
```python
from app.service import detect_language

result = detect_language("Cześć, jak się masz?")
# {'language': 'pl', 'language_name': 'Polish', 'confidence': 0.98}
```

**Przypadki użycia**:
- Automatyczne ustawienie języka interfejsu
- Routing wiadomości do odpowiedniego agenta
- Analiza statystyk dotyczących języków
- Filtrowanie treści

---

## 2. Rozpoznawanie mowy (ASR) 🎤

Transkrypcja audio na tekst z automatyczną detekcją języka.

**Jak to działa**:
- System otrzymuje plik audio
- Używa modelu `faster-whisper` do transkrypcji
- Model automatycznie rozpoznaje język audio
- Zwraca transkrypcję oraz kod języka

**Obsługiwane formaty audio**:
- WAV, MP3, OGG, FLAC, M4A, AIFF, OPUS

**Modele dostępne**:
- `tiny` - najszybszy, najmniej dokładny (~1GB VRAM)
- `base` - balans szybkości i dokładności (~1GB VRAM) - **domyślny**
- `small` - więcej dokładności (~2GB VRAM)
- `medium` - wysoka dokładność (~5GB VRAM)
- `large` - najwyższa dokładność (~10GB VRAM)

**Przykład**:
```python
from app.asr_service import transcribe_audio_with_segments

result = transcribe_audio_with_segments("recording.wav")
# {
#   'transcription': 'Hello world',
#   'language': 'en',
#   'language_name': 'English',
#   'confidence': 0.92
# }
```

**Przypadki użycia**:
- Interfejs głosowy
- Transkrypcja nagrań
- Asystenci głosowi
- Automatyczne podpisy do filmów

---

## 3. Dialog - Odpowiedzi dostosowane do języka 💬

System udziela odpowiedzi dialogowych w tym samym języku, w którym został zaadresowany.

**Jak to działa**:
- System wykrywa język wejścia
- Zwraca predefiniowaną odpowiedź w tym samym języku
- Odpowiedzi są dostosowane do kontekstu

**Wspierane odpowiedzi**:
- Powitania
- Odpowiedzi na pytania
- Rozstania

**Przykład**:
```python
from app.service import detect_language

# Język angielski
result = detect_language("Hello")  # → "Hello! How can I help you?"

# Język polski
result = detect_language("Cześć")  # → "Cześć! Jak się masz?"

# Język niemiecki
result = detect_language("Guten Tag")  # → "Guten Tag! Wie kann ich dir helfen?"
```

**Wspierane języki w dialogu**:
- 🇬🇧 English
- 🇵🇱 Polish
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇫🇷 French
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇯🇵 Japanese
- 🇨🇳 Chinese
- 🇰🇷 Korean
- I wiele innych...

**Przypadki użycia**:
- Chatboty wielojęzyczne
- Asystenci wirtualni
- Automatyczne odpowiadanie
- Powitania systemu w rodzimym języku użytkownika

---

## 4. Detekcja Code-Switching 🔀

Identyfikacja zmiany języka (code-switching) w tekście.

**Co to jest code-switching?**

Code-switching to zjawisko, gdy osób wielojęzyczna w jednej wypowiedzi używa słów lub fraz z dwóch lub więcej języków. Przykład:

```
"Hello, jak się masz? Good morning"
```

W tym tekście są elementy z trzech języków:
- "Hello" - angielski
- "jak się masz?" - polski
- "Good morning" - angielski

**Jak to działa**:
- System analizuje tekst fragmentami
- Dla każdego fragmentu wykrywa język
- Identyfikuje zmiany między językami
- Zwraca szczegółowy raport

**Przykład**:
```python
from app.service import detect_code_switching

text = "Hello, jak się masz? Good morning"
result = detect_code_switching(text)

# {
#   'code_switching_detected': True,
#   'languages_detected': ['en', 'pl'],
#   'segments': [
#     {'text': 'Hello', 'language': 'en', 'language_name': 'English'},
#     {'text': 'jak się masz', 'language': 'pl', 'language_name': 'Polish'},
#     {'text': 'Good morning', 'language': 'en', 'language_name': 'English'}
#   ]
# }
```

**Przypadki użycia**:
- Analiza mowy wielojęzycznih użytkowników
- Badania lingwistyczne
- Adaptacyjne interfejsy użytkownika
- Identyfikacja preferencji językowych
- Tłumaczenie asystowane
- Analiza nagrań z rozmów międzynarodowych

---

## 5. Lista obsługiwanych języków 📊

Pobranie pełnej listy wszystkich obsługiwanych języków i kodów.

**Jak to działa**:
- Zwraca mapę wszystkich dostępnych par kod-nazwa
- Przydatne do inicjalizacji interfejsu użytkownika

**Przykład**:
```python
from app.service import LANGUAGE_MAP

print(LANGUAGE_MAP)
# {
#   'en': 'English',
#   'pl': 'Polish',
#   'es': 'Spanish',
#   'de': 'German',
#   ...
# }
```

---

## 6. System Health Check ✅

Sprawdzenie stanu i dostępności systemu.

**Jak to działa**:
- Zwraca status dostępności systemu
- Przydatne do monitorowania

**Odpowiedź**:
```json
{"status": "ok"}
```

---

## Kombinacje funkcji

Funkcje mogą być łączone do bardziej zaawansowanych scenariuszy:

### Scenariusz 1: Pełny przepływ głosu
1. Użytkownik nagrywa wiadomość
2. **ASR** transkrybuje audio i wykrywa język
3. **Dialog** udziela odpowiedzi w tym samym języku
4. System może też uruchomić **code-switching detection** jeśli jest to wymagane

### Scenariusz 2: Analiza wielojęzycznych konwersacji
1. Odbierz transkrypcję rozmowy
2. Użyj **Code-Switching Detection** do zidentyfikowania zmian
3. Analizuj wzorce użycia języków między użytkownikami
4. Dostosuj ustawienia interfejsu na podstawie preferencji

### Scenariusz 3: Inteligentny chatbot
1. Odbierz wiadomość
2. **Detect Language** z tekstu
3. Udziel odpowiedzi dialogowej w tym samym języku
4. Opcjonalnie: Udziel tłumaczenia na drugi preferowany język

---

## Wydajność

| Funkcja | Czas wykonania | Notatka |
|---------|---------------|--------|
| Detekcja języka (tekst) | ~10ms | Bardzo szybko |
| ASR (1 sekunda audio) | ~500ms | Zależy od modelu |
| Dialog | ~5ms | Natychmiastowo |
| Code-Switching (100 znaków) | ~50ms | Szybko |

---

## Limitacje

- **Detekcja języka**: Najlepsza dla tekstu ~50+ znaków
- **ASR**: Wymaga wyraźnej mowy, najlepiej bez tła
- **Code-Switching**: Działa na poziomie fragmentów, może mieć trudności z bardzo krótkimi fragmentami
- **Dialog**: Tylko predefiniowane odpowiedzi, brak pełnego NLU
