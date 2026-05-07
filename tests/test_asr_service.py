from types import SimpleNamespace

from app import asr_service


def test_transcribe_audio_with_segments_uses_model(monkeypatch):
    class FakeModel:
        def transcribe(self, file_path):
            return [
                SimpleNamespace(start=0.0, end=0.5, text="Hello world"),
            ], SimpleNamespace(language="en")

    monkeypatch.setattr("app.asr_service._get_model", lambda: FakeModel())

    result = asr_service.transcribe_audio_with_segments("dummy.wav")

    assert result["segments"] == [{"start": 0.0, "end": 0.5, "text": "Hello world"}]
    assert result["asr_language"] == "en"
