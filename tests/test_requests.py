import requests 

response = requests.post(
    "http://127.0.0.1:8000/detect-language/text",
    json={"text": "Hello world"}
)

print(response.json())