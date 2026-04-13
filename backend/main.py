from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

NCERT_CHUNKS = [
    {"id": "sci_1", "text": "Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to make food and release oxygen.", "subject": "Science"},
    {"id": "sci_2", "text": "Mitochondria is called the powerhouse of the cell because it produces energy as ATP through cellular respiration.", "subject": "Science"},
    {"id": "sci_3", "text": "Newton First Law: object at rest stays at rest unless acted upon by external force.", "subject": "Science"},
    {"id": "sci_4", "text": "Newton Second Law: Force equals mass times acceleration. F = ma.", "subject": "Science"},
    {"id": "sci_5", "text": "Newton Third Law: for every action there is an equal and opposite reaction.", "subject": "Science"},
    {"id": "sci_6", "text": "Ozone layer in stratosphere protects Earth from harmful ultraviolet radiation.", "subject": "Science"},
    {"id": "sci_7", "text": "Global warming is caused by greenhouse gases like CO2 trapping heat in atmosphere.", "subject": "Science"},
    {"id": "sci_8", "text": "Human body has 206 bones. Smallest is stapes in ear, largest is femur in thigh.", "subject": "Science"},
    {"id": "sci_9", "text": "Speed of light is 3 x 10 to the power 8 metres per second.", "subject": "Science"},
    {"id": "sci_10", "text": "Acids have pH less than 7, bases greater than 7, neutral is pH 7.", "subject": "Science"},
    {"id": "math_1", "text": "Pythagorean theorem: a squared plus b squared equals c squared in a right triangle.", "subject": "Mathematics"},
    {"id": "math_2", "text": "Area of circle is pi times radius squared. Circumference is 2 pi r. Pi is 3.14159.", "subject": "Mathematics"},
    {"id": "math_3", "text": "Quadratic equation: ax squared plus bx plus c equals 0.", "subject": "Mathematics"},
    {"id": "math_4", "text": "Simple Interest = Principal times Rate times Time divided by 100.", "subject": "Mathematics"},
    {"id": "math_5", "text": "HCF is largest number dividing two numbers. LCM is smallest number divisible by both.", "subject": "Mathematics"},
    {"id": "math_6", "text": "Probability = favourable outcomes divided by total outcomes. Ranges from 0 to 1.", "subject": "Mathematics"},
    {"id": "tamil_1", "text": "Thirukkural written by Thiruvalluvar has 1330 kurals in three sections: Aram, Porul, Inbam.", "subject": "Tamil"},
    {"id": "tamil_2", "text": "Silappatikaram is Tamil epic by Ilango Adigal about Kovalan and Kannagi.", "subject": "Tamil"},
    {"id": "tamil_3", "text": "Tamil classical language has 2000 years of history. Alphabet has 247 letters.", "subject": "Tamil"},
    {"id": "tamil_4", "text": "Kambaramayanam is Tamil version of Ramayana by poet Kambar.", "subject": "Tamil"},
    {"id": "evs_1", "text": "Deforestation removes forests causing biodiversity loss, soil erosion, climate change.", "subject": "EVS"},
    {"id": "evs_2", "text": "Solar, wind, hydroelectric are renewable energy. Coal and petroleum are non-renewable.", "subject": "EVS"},
    {"id": "evs_3", "text": "Water cycle: evaporation, condensation, precipitation, collection.", "subject": "EVS"},
    {"id": "evs_4", "text": "Biodiversity is variety of life on Earth. Important for ecosystem balance.", "subject": "EVS"},
    {"id": "evs_5", "text": "Acid rain caused by sulphur dioxide and nitrogen oxides from factories.", "subject": "EVS"},
]

def simple_search(query, top_k=3):
    query_words = set(query.lower().split())
    scored = []
    for chunk in NCERT_CHUNKS:
        chunk_words = set(chunk["text"].lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk["text"]))
    scored.sort(reverse=True)
    return [text for score, text in scored[:top_k] if score > 0]

class Query(BaseModel):
    question: str

class QuizRequest(BaseModel):
    subject: str
    grade: str

@app.get("/")
def home():
    return {"message": "IncluPlayAI with Groq AI Running!"}

@app.post("/ask")
async def ask_question(query: Query):
    try:
        chunks = simple_search(query.question, top_k=3)
        context = "\n".join(chunks)
        if context:
            prompt = "You are a friendly NCERT tutor for Indian students Grade 6-10. Use this context:\n" + context + "\n\nAnswer in 2-3 simple sentences: " + query.question
        else:
            prompt = "You are a friendly NCERT tutor for Indian students Grade 6-10. Answer in 2-3 simple sentences: " + query.question

        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": "Bearer " + GROQ_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300
            },
            timeout=15
        )
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return {"answer": answer, "rag_used": len(chunks) > 0}
    except Exception as e:
        return {"answer": "Error: " + str(e), "rag_used": False}

@app.post("/quiz")
async def generate_quiz(req: QuizRequest):
    try:
        content = "Generate 5 multiple choice questions for " + req.subject + " for " + req.grade + " NCERT students. Return ONLY JSON array: [{\"q\": \"question\", \"options\": [\"A\",\"B\",\"C\",\"D\"], \"answer\": \"correct\"}]"
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": "Bearer " + GROQ_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": content}],
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            questions = json.loads(match.group())
            return {"questions": questions}
        return {"questions": []}
    except Exception as e:
        return {"questions": [], "error": str(e)}