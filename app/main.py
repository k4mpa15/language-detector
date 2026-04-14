from fastapi import FastAPI, Request
from app.service import LANGUAGE_MAP, detect_language

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


# @app.post("/detect-code-switching")


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
            response_text = f"Wykryty język: {language_name}. Na razie mam przygotowaną pełną obsługę głównie dla PL, EN i DE."

        return {"detected_language": language, "response_text": response_text}

    except Exception as e:
        return {"error": str(e)}
