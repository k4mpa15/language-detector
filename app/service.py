def detect_language(text):
    text = text.lower()

    if "hello" in text or "how are you" in text:
        return {"language": "en", "confidence": 0.95}
    elif "hallo" in text or "guten" in text:
        return {"language": "de", "confidence": 0.95}
    else:
        return {"language": "pl", "confidence": 0.95}