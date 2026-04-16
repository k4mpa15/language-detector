from fastapi import FastAPI, Request
from app.service import LANGUAGE_MAP, detect_language, detect_code_switching

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

        cleaned_utterances = [u.strip() for u in utterances if isinstance(u, str) and u.strip()]

        if not cleaned_utterances:
            return {"error": "Lista 'utterances' nie może być pusta"}

        return detect_code_switching(cleaned_utterances)

    except Exception as e:
        return {"error": str(e)}


@app.post("/detect-language/voice")
async def detect_language_voice():
    return {"message": "Voice detection not implemented yet"}


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
            response_text = (
                "I detected English. I can continue the conversation in English."
            )
        elif language == "de":
            response_text = "Ich habe Deutsch erkannt. Ich kann das Gespräch auf Deutsch fortsetzen."
        else:
            response_text = f"Detected language: {language_name}. Full dialog support is currently focused on Polish, English and German."
        return {
        "detected_language": language,
        "language_name": language_name,
        "response_text": response_text
}

    except Exception as e:
        return {"error": str(e)}
