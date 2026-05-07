_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as e:
            raise RuntimeError(
                "faster-whisper is required for audio transcription. Install it with requirements."
            ) from e

        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model


def transcribe_audio_with_segments(file_path):
    model = _get_model()
    segments, info = model.transcribe(file_path)

    result_segments = []

    for segment in segments:
        result_segments.append(
            {"start": segment.start, "end": segment.end, "text": segment.text.strip()}
        )

    return {"segments": result_segments, "asr_language": info.language}
