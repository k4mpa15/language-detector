from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")


def transcribe_audio(file_path):
    segments, info = model.transcribe(file_path)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return {
        "transcription": text.strip(),
        "asr_language": info.language
    }