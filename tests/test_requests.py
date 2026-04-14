import requests

base_url = "http://127.0.0.1:8000"

response1 = requests.post(
    f"{base_url}/detect-language/text", json={"text": "Hello world"}
)

print("detect-language/text")
print(response1.status_code)
print(response1.json())
print()

response2 = requests.post(
    f"{base_url}/dialog/respond", json={"text": "parte como estas"}
)

print("dialog/respond")
print(response2.status_code)
print(response2.json())
