from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")


def transcribe_audio_with_segments(file_path):
    segments, info = model.transcribe(file_path)

    result_segments = []

    for segment in segments:
        result_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return {
        "segments": result_segments,
        "asr_language": info.language
    }