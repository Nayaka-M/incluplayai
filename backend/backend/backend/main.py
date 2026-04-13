from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="IncluPlayAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = "AIzaSyC8IF7VRpzG8O_3srNoZ6iA9wXtdkKCMtE"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "IncluPlayAI Backend Running!"}

@app.post("/ask")
async def ask_question(query: Query):
    try:
        response = requests.post(
            GEMINI_URL + "?key=" + GEMINI_API_KEY,
            json={
                "contents": [{
                    "parts": [{
                        "text": "You are an NCERT tutor for Indian school students Grades 6 to 10. Answer clearly in 2 to 3 simple sentences: " + query.question
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 300,
                    "temperature": 0.7
                }
            },
            timeout=15
        )
        data = response.json()

        if "candidates" in data:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"answer": answer}
        elif "error" in data:
            return {"answer": "Gemini error: " + data["error"]["message"]}
        else:
            return {"answer": "Unexpected response: " + str(data)}

    except Exception as e:
        return {"answer": "Error: " + str(e)}