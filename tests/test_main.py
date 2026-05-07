from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_json(path):
    response = client.get(path)
    assert response.status_code == 200
    return response.json()


def post_json(path, payload):
    response = client.post(path, json=payload)
    assert response.status_code == 200
    return response.json()


def assert_has_fields(data, *fields):
    for field in fields:
        assert field in data


def test_health_endpoint():
    assert get_json("/health") == {"status": "ok"}


def test_supported_languages_endpoint():
    languages = get_json("/supported-languages")["supported_languages"]
    assert isinstance(languages, list)
    assert any(lang["code"] == "pl" for lang in languages)
    assert any(lang["code"] == "en" for lang in languages)


def test_detect_language_text_endpoint():
    data = post_json(
        "/detect-language/text",
        {"text": "Hello, how are you today? Please let me know how are you feeling"},
    )

    assert data["language"] == "en"
    assert data["language_name"] == "English"
    assert_has_fields(data, "confidence")


def test_detect_code_switching_endpoint():
    data = post_json(
        "/detect-code-switching",
        {
            "utterances": [
                "Cześć, jak się masz?",
                "I am fine, thank you.",
                "Super, to dobrze.",
            ]
        },
    )

    assert data["code_switch_detected"] is True
    assert isinstance(data["switch_points"], list)
    assert isinstance(data["sequence"], list)
    assert len(data["sequence"]) == 3


def test_dialog_respond_endpoint_polish():
    data = post_json("/dialog/respond", {"text": "Cześć, jak się masz?"})
    assert data["language"] == "pl"
    assert data["language_name"] == "Polish"
    assert "Mogę kontynuować rozmowę po polsku" in data["response_text"]


def test_detect_language_text_requires_text():
    data = post_json("/detect-language/text", {})
    assert data["error"] == "Pole 'text' jest wymagane"


def test_detect_code_switching_requires_utterances():
    data = post_json("/detect-code-switching", {})
    assert data["error"] == "Pole 'utterances' jest wymagane"


def test_detect_code_switching_requires_list():
    data = post_json("/detect-code-switching", {"utterances": "not a list"})
    assert data["error"] == "Pole 'utterances' musi być listą"


def test_detect_code_switching_requires_non_empty_list():
    data = post_json("/detect-code-switching", {"utterances": ["", "   "]})
    assert data["error"] == "Lista 'utterances' nie może być pusta"


def test_dialog_respond_requires_text():
    data = post_json("/dialog/respond", {})
    assert data["error"] == "Pole 'text' jest wymagane"


def test_detect_language_voice_endpoint_with_mock(monkeypatch):
    def fake_transcribe_audio_with_segments(path):
        return {
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "Hello, how are you?"},
                {"start": 1.0, "end": 2.0, "text": "Cześć, jak się masz?"},
            ]
        }

    def fake_detect_language(text):
        if "Cześć" in text:
            return {"language": "pl", "language_name": "Polish", "confidence": 0.98}
        return {"language": "en", "language_name": "English", "confidence": 0.99}

    monkeypatch.setattr(
        "app.main.transcribe_audio_with_segments", fake_transcribe_audio_with_segments
    )
    monkeypatch.setattr("app.main.detect_language", fake_detect_language)

    response = client.post(
        "/detect-language/voice",
        files={"file": ("audio.wav", b"dummy audio data", "audio/wav")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "pl"
    assert data["language_name"] == "Polish"
    assert data["code_switch_detected"] is True
    assert isinstance(data["sequence"], list)
    assert len(data["sequence"]) == 2
    assert data["sequence"][0]["language"] == "en"
    assert data["sequence"][1]["language"] == "pl"
