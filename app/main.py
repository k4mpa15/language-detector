from fastapi import FastAPI, Request, UploadFile, File
from app.service import LANGUAGE_MAP, detect_language, detect_code_switching
from app.asr_service import transcribe_audio_with_segments 
import os
import tempfile

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/supported-languages")
def supported_languages():
    languages = []

    for code, name in LANGUAGE_MAP.items():
        languages.append({"code": code, "name": name})

    return {"supported_languages": languages}


@app.post("/detect-language/text")
async def detect_language_text(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return {"error": "Pole 'text' jest wymagane"}

        return detect_language(text)

    except Exception as e:
        return {"error": str(e)}


@app.post("/detect-code-switching")
async def detect_code_switching_endpoint(request: Request):
    try:
        data = await request.json()
        utterances = data.get("utterances", [])

        if not utterances:
            return {"error": "Pole 'utterances' jest wymagane"}

        if not isinstance(utterances, list):
            return {"error": "Pole 'utterances' musi być listą"}

        cleaned_utterances = [
            u.strip() for u in utterances if isinstance(u, str) and u.strip()
        ]

        if not cleaned_utterances:
            return {"error": "Lista 'utterances' nie może być pusta"}

        return detect_code_switching(cleaned_utterances)

    except Exception as e:
        return {"error": str(e)}


@app.post("/detect-language/voice")
async def detect_language_voice(file: UploadFile = File(...)):
    try:
        if not file.filename:
            return {"error": "No file provided"}

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # ASR z segmentami
        asr_result = transcribe_audio_with_segments(temp_path)
        os.remove(temp_path)

        segments = asr_result["segments"]

        if not segments:
            return {"error": "No speech detected"}

        sequence = []
        switch_points = []

        for seg in segments:
            text = seg["text"]

            if not text:
                continue

            lid = detect_language(text)

            if "error" in lid:
                lang = "unknown"
                lang_name = "Unknown"
            else:
                lang = lid["language"]
                lang_name = lid["language_name"]

            sequence.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": text,
                "language": lang,
                "language_name": lang_name
            })

        # detect switching
        for i in range(1, len(sequence)):
            if sequence[i]["language"] != sequence[i - 1]["language"]:
                switch_points.append(i)

        full_text = " ".join([s["text"] for s in sequence])

        return {
            "transcription": full_text,
            "code_switch_detected": len(switch_points) > 0,
            "switch_points": switch_points,
            "sequence": sequence
        }

    except Exception as e:
        return {"error": str(e)}
    
    
@app.post("/dialog/respond")
async def dialog_respond(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return {"error": "Pole 'text' jest wymagane"}

        result = detect_language(text)

        if "error" in result:
            return result

        language = result["language"]
        language_name = result["language_name"]

        if language == "pl":
            response_text = "Wykryłam język polski. Mogę kontynuować rozmowę po polsku."
        elif language == "en":
            response_text = "I detected English. I can continue the conversation in English."
        elif language == "de":
            response_text = "Ich habe Deutsch erkannt. Ich kann das Gespräch auf Deutsch fortsetzen."
        else:
            response_text = f"Detected language: {language_name}. Full dialog support is currently focused on Polish, English and German."
        return {
            "language": language,
            "language_name": language_name,
            "response_text": response_text,
        }

    except Exception as e:
        return {"error": str(e)}
