import requests

BASE_URL = "http://127.0.0.1:8000"


def get_response(path):
    response = requests.get(f"{BASE_URL}{path}")
    assert response.status_code == 200
    return response


def post_json(path, payload):
    response = requests.post(f"{BASE_URL}{path}", json=payload)
    assert response.status_code == 200
    return response


def post_file(path, file_path, file_field="file"):
    with open(file_path, "rb") as file_obj:
        response = requests.post(f"{BASE_URL}{path}", files={file_field: file_obj})
    assert response.status_code == 200
    return response


def assert_has_fields(data, *fields):
    for field in fields:
        assert field in data


def print_response(title, response):
    print(f"\n--- {title} ---")
    print("Status code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response text:", response.text)


def run_requests():
    response = get_response("/health")
    print_response("GET /health", response)
    assert response.json()["status"] == "ok"

    response = get_response("/supported-languages")
    print_response("GET /supported-languages", response)
    data = response.json()
    assert isinstance(data["supported_languages"], list)

    response = post_json("/detect-language/text", {"text": "Hello world"})
    print_response("POST /detect-language/text", response)
    data = response.json()
    assert_has_fields(data, "language", "language_name", "confidence")

    response = post_json("/dialog/respond", {"text": "Cześć, jak się masz?"})
    print_response("POST /dialog/respond", response)
    data = response.json()
    assert_has_fields(data, "language", "language_name", "response_text")

    response = post_json(
        "/detect-code-switching",
        {
            "utterances": [
                "Cześć, jak się masz?",
                "I am fine, thank you.",
                "Super, to dobrze.",
            ]
        },
    )
    print_response("POST /detect-code-switching", response)
    data = response.json()
    assert_has_fields(data, "code_switch_detected", "switch_points", "sequence")
    assert isinstance(data["sequence"], list)

    response = post_file("/detect-language/voice", "tests/sample_pl_en.m4a")
    print_response("POST /detect-language/voice", response)
    data = response.json()
    assert_has_fields(
        data,
        "transcription",
        "language",
        "language_name",
        "code_switch_detected",
        "sequence",
    )


if __name__ == "__main__":
    run_requests()
