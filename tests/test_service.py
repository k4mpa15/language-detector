from app.service import detect_language, detect_code_switching, LANGUAGE_MAP


def test_language_map_contains_required_languages():
    assert "en" in LANGUAGE_MAP
    assert "pl" in LANGUAGE_MAP
    assert "de" in LANGUAGE_MAP


def test_detect_language_english():
    result = detect_language("Hello, how are you today?")

    assert "language" in result
    assert "language_name" in result
    assert "confidence" in result
    assert result["language"] == "en"


def test_detect_language_polish():
    result = detect_language("Cześć, jak się dzisiaj masz?")

    assert "language" in result
    assert "language_name" in result
    assert "confidence" in result
    assert result["language"] == "pl"


def test_detect_language_german():
    result = detect_language("Hallo, wie geht es dir heute?")

    assert "language" in result
    assert "language_name" in result
    assert "confidence" in result
    assert result["language"] == "de"


def test_detect_code_switching_detects_change():
    result = detect_code_switching([
        "Cześć, jak się masz?",
        "I am fine, thank you.",
        "Super, to dobrze."
    ])

    assert result["code_switch_detected"] is True
    assert "switch_points" in result
    assert len(result["switch_points"]) >= 1
    assert len(result["sequence"]) == 3


def test_detect_code_switching_no_change():
    result = detect_code_switching([
        "Hello, how are you?",
        "I am fine, thank you.",
        "This is a test."
    ])

    assert result["code_switch_detected"] is False
    assert result["switch_points"] == []
    assert len(result["sequence"]) == 3