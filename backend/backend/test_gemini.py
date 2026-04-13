import requests

GEMINI_API_KEY = "AIzaSyC8IF7VRpzG8O_3srNoZ6iA9wXtdkKCMtE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

response = requests.post(
    GEMINI_URL + "?key=" + GEMINI_API_KEY,
    json={
        "contents": [{
            "parts": [{
                "text": "What is photosynthesis? Answer in 2 sentences."
            }]
        }]
    },
    timeout=15
)

print("Status:", response.status_code)
print("Response:", response.json())