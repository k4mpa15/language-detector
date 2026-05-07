import pytest

from app.service import detect_code_switching, detect_language, LANGUAGE_MAP


def assert_language_result(result, expected_language, expected_name):
    assert result["language"] == expected_language
    assert result["language_name"] == expected_name
    assert isinstance(result["confidence"], float)


def assert_code_switching_result(result, expected_switch, utterance_count):
    assert result["code_switch_detected"] is expected_switch
    assert isinstance(result["switch_points"], list)
    assert isinstance(result["sequence"], list)
    assert len(result["sequence"]) == utterance_count
    if expected_switch:
        assert len(result["switch_points"]) >= 1
    else:
        assert result["switch_points"] == []


@pytest.mark.parametrize(
    "text,expected_language,expected_name",
    [
        (
            "Hello, how are you today? Please let me know how are you feeling",
            "en",
            "English",
        ),
        ("Cześć, jak się dzisiaj masz?", "pl", "Polish"),
        ("Hallo, wie geht es dir heute?", "de", "German"),
    ],
)
def test_detect_language(text, expected_language, expected_name):
    result = detect_language(text)
    assert_language_result(result, expected_language, expected_name)


def test_language_map_contains_required_languages():
    assert set(["en", "pl", "de"]).issubset(LANGUAGE_MAP)


@pytest.mark.parametrize(
    "utterances,expected_switch",
    [
        (
            [
                "Cześć, jak się masz?",
                "I am fine, thank you.",
                "Super, to dobrze.",
            ],
            True,
        ),
        (
            [
                "Hello, how are you?",
                "I am fine, thank you.",
                "This is a test.",
            ],
            False,
        ),
    ],
)
def test_detect_code_switching(utterances, expected_switch):
    result = detect_code_switching(utterances)
    assert_code_switching_result(result, expected_switch, len(utterances))
