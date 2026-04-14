from fastapi import FastAPI, Request
from app.service import detect_language

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


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