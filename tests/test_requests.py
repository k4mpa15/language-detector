import requests

BASE_URL = "http://127.0.0.1:8000"


def print_response(title, response):
    print(f"\n--- {title} ---")
    print("Status code:", response.status_code)

    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response text:", response.text)


# 1. GET /health
response = requests.get(f"{BASE_URL}/health")
print_response("GET /health", response)
assert response.status_code == 200
assert response.json()["status"] == "ok"


# 2. GET /supported-languages
response = requests.get(f"{BASE_URL}/supported-languages")
print_response("GET /supported-languages", response)
assert response.status_code == 200
assert "supported_languages" in response.json()
assert isinstance(response.json()["supported_languages"], list)


# 3. POST /detect-language/text
response = requests.post(
    f"{BASE_URL}/detect-language/text",
    json={"text": "Hello world"}
)
print_response("POST /detect-language/text", response)
data = response.json()

assert response.status_code == 200
assert "language" in data
assert "language_name" in data
assert "confidence" in data


# 4. POST /dialog/respond
response = requests.post(
    f"{BASE_URL}/dialog/respond",
    json={"text": "Cześć, jak się masz?"}
)
print_response("POST /dialog/respond", response)
data = response.json()

assert response.status_code == 200
assert "language" in data
assert "language_name" in data
assert "response_text" in data


# 5. POST /detect-code-switching
response = requests.post(
    f"{BASE_URL}/detect-code-switching",
    json={
        "utterances": [
            "Cześć, jak się masz?",
            "I am fine, thank you.",
            "Super, to dobrze.",
        ]
    },
)
print_response("POST /detect-code-switching", response)
data = response.json()

assert response.status_code == 200
assert "code_switch_detected" in data
assert "switch_points" in data
assert "sequence" in data
assert isinstance(data["sequence"], list)


# 6. POST /detect-language/voice
with open("tests/sample_pl_en.m4a", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/detect-language/voice",
        files={"file": f}
    )

print_response("POST /detect-language/voice", response)
data = response.json()

assert response.status_code == 200
assert "transcription" in data
assert "language" in data
assert "language_name" in data
assert "code_switch_detected" in data
assert "sequence" in data