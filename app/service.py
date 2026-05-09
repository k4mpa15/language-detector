from langdetect import detect_langs, DetectorFactory

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
    "pl": "Polish",
}

# Responses for each language
LANGUAGE_RESPONSES = {
    "pl": "Wykryłam język polski. Mogę kontynuować rozmowę po polsku. 🇵🇱",
    "en": "I detected English. I can continue the conversation in English. 🇬🇧",
    "de": "Ich habe Deutsch erkannt. Ich kann das Gespräch auf Deutsch fortsetzen. 🇩🇪",
    "es": "Detecté español. Puedo continuar la conversación en español. 🇪🇸",
    "fr": "J'ai détecté le français. Je peux continuer la conversation en français. 🇫🇷",
    "pt": "Detectei português. Posso continuar a conversa em português. 🇧🇷",
    "ru": "Я обнаружил русский язык. Я могу продолжить разговор на русском. 🇷🇺",
    "ar": "لقد اكتشفت العربية. يمكنني متابعة المحادثة بالعربية. 🇸🇦",
    "hi": "मैंने हिंदी का पता लगाया। मैं हिंदी में बातचीत जारी रख सकता हूँ। 🇮🇳",
    "zh-cn": "我检测到了中文。我可以继续用中文交谈。 🇨🇳",
}


def detect_language(text):
    try:
        langs = detect_langs(text)
        best = langs[0]

        language_code = best.lang
        confidence = best.prob

        language_name = LANGUAGE_MAP.get(language_code, f"Unknown ({language_code})")

        return {
            "language": language_code,
            "language_name": language_name,
            "confidence": round(confidence, 3),
        }

    except Exception as e:
        return {"error": f"Language detection failed: {str(e)}"}


def detect_code_switching(utterances):
    sequence = []
    switch_points = []

    for utterance in utterances:
        result = detect_language(utterance)

        if "error" in result:
            sequence.append(
                {"text": utterance, "language": "unknown", "language_name": "Unknown"}
            )
        else:
            sequence.append(
                {
                    "text": utterance,
                    "language": result["language"],
                    "language_name": result["language_name"],
                    "confidence": result.get("confidence"),
                }
            )

    for i in range(1, len(sequence)):
        if sequence[i]["language"] != sequence[i - 1]["language"]:
            switch_points.append(i)

    return {
        "code_switch_detected": len(switch_points) > 0,
        "switch_points": switch_points,
        "sequence": sequence,
    }
