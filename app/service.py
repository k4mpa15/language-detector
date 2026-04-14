from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

LANGUAGE_MAP = {
    "en": "English",
    "zh-cn": "Chinese (Simplified)",
    "es": "Spanish",
    "hi": "Hindi",
    "ar": "Arabic",
    "fr": "French",
    "pt": "Portuguese",
    "ru": "Russian",
    "de": "German",
    "pl": "Polish"
}

def detect_language(text):
    try:
        language_code = detect(text)
        language_name = LANGUAGE_MAP.get(language_code, f"Unknown ({language_code})")

        return {
            "language": language_code,
            "language_name": language_name
        }
    except Exception as e:
        return {
            "error": f"Language detection failed: {str(e)}"
        }
    