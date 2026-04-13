from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import re
import json
import os
import numpy as np
from dotenv import load_dotenv
from endee import Endee

load_dotenv()

app = FastAPI(title="IncluPlayAI - Endee Vector DB + Groq AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

NCERT_CHUNKS = [
    {"id": "sci_1",  "text": "Photosynthesis is the process by which green plants use sunlight, water, and carbon dioxide to make food and release oxygen.", "subject": "Science", "topic": "Photosynthesis"},
    {"id": "sci_2",  "text": "Mitochondria is called the powerhouse of the cell because it produces energy as ATP through cellular respiration.", "subject": "Science", "topic": "Cell Biology"},
    {"id": "sci_3",  "text": "Newton First Law: An object at rest stays at rest unless acted upon by an external force.", "subject": "Science", "topic": "Laws of Motion"},
    {"id": "sci_4",  "text": "Newton Second Law: Force equals mass times acceleration. F = ma.", "subject": "Science", "topic": "Laws of Motion"},
    {"id": "sci_5",  "text": "Newton Third Law: For every action there is an equal and opposite reaction.", "subject": "Science", "topic": "Laws of Motion"},
    {"id": "sci_6",  "text": "The ozone layer in the stratosphere protects Earth from harmful ultraviolet radiation from the sun.", "subject": "Science", "topic": "Environment"},
    {"id": "sci_7",  "text": "Global warming is caused by greenhouse gases like CO2 and methane trapping heat in the atmosphere.", "subject": "Science", "topic": "Environment"},
    {"id": "sci_8",  "text": "The human body has 206 bones. The smallest bone is the stapes in the ear. The largest bone is the femur.", "subject": "Science", "topic": "Human Body"},
    {"id": "sci_9",  "text": "The speed of light in vacuum is approximately 3 x 10 to the power 8 metres per second.", "subject": "Science", "topic": "Light"},
    {"id": "sci_10", "text": "Acids have pH less than 7. Bases have pH greater than 7. Neutral substances have pH equal to 7.", "subject": "Science", "topic": "Acids and Bases"},
    {"id": "sci_11", "text": "The cell is the basic unit of life. Plant cells have cell wall and chloroplasts. Animal cells do not have cell wall.", "subject": "Science", "topic": "Cell Biology"},
    {"id": "sci_12", "text": "Sound travels as longitudinal waves. Sound cannot travel in vacuum. Sound travels faster in solids.", "subject": "Science", "topic": "Sound"},
    {"id": "sci_13", "text": "Digestion breaks down food into nutrients. Stomach produces acid to digest food. Small intestine absorbs nutrients.", "subject": "Science", "topic": "Human Body"},
    {"id": "sci_14", "text": "Evaporation is when liquid turns to gas. Condensation is when gas turns to liquid.", "subject": "Science", "topic": "Matter"},
    {"id": "sci_15", "text": "Magnetic field lines go from north pole to south pole. Earth itself acts like a giant magnet.", "subject": "Science", "topic": "Magnetism"},
    {"id": "math_1", "text": "Pythagorean theorem: in a right triangle a squared plus b squared equals c squared.", "subject": "Mathematics", "topic": "Geometry"},
    {"id": "math_2", "text": "Area of circle is pi times radius squared. Circumference is 2 pi r. Pi is approximately 3.14159.", "subject": "Mathematics", "topic": "Mensuration"},
    {"id": "math_3", "text": "Quadratic equation has the form ax squared plus bx plus c equals 0.", "subject": "Mathematics", "topic": "Algebra"},
    {"id": "math_4", "text": "Simple Interest equals Principal times Rate times Time divided by 100.", "subject": "Mathematics", "topic": "Commercial Maths"},
    {"id": "math_5", "text": "HCF is the largest number that divides two numbers exactly. LCM is the smallest number divisible by both.", "subject": "Mathematics", "topic": "Number Theory"},
    {"id": "math_6", "text": "Probability equals number of favourable outcomes divided by total outcomes. Ranges from 0 to 1.", "subject": "Mathematics", "topic": "Probability"},
    {"id": "math_7", "text": "Area of triangle is half times base times height. Perimeter is sum of all three sides.", "subject": "Mathematics", "topic": "Geometry"},
    {"id": "math_8", "text": "Volume of cylinder is pi times radius squared times height.", "subject": "Mathematics", "topic": "Mensuration"},
    {"id": "math_9", "text": "Percentage means per hundred. To find percentage divide part by whole and multiply by 100.", "subject": "Mathematics", "topic": "Commercial Maths"},
    {"id": "math_10","text": "Arithmetic progression has a common difference between consecutive terms.", "subject": "Mathematics", "topic": "Progressions"},
    {"id": "tamil_1","text": "Thirukkural was written by Thiruvalluvar. It contains 1330 kurals in three sections: Aram, Porul, and Inbam.", "subject": "Tamil", "topic": "Literature"},
    {"id": "tamil_2","text": "Silappatikaram is one of the five great Tamil epics written by Ilango Adigal about Kovalan and Kannagi.", "subject": "Tamil", "topic": "Literature"},
    {"id": "tamil_3","text": "Tamil is a classical language with over 2000 years of literary history. The Tamil alphabet has 247 letters.", "subject": "Tamil", "topic": "Language"},
    {"id": "tamil_4","text": "Kambaramayanam is the Tamil version of Ramayana written by the poet Kambar.", "subject": "Tamil", "topic": "Literature"},
    {"id": "tamil_5","text": "Avvaiyar was a famous Tamil poet who wrote Aathichudi and Konrai Vendan for children.", "subject": "Tamil", "topic": "Literature"},
    {"id": "evs_1",  "text": "Deforestation is the removal of forests causing biodiversity loss, soil erosion, and climate change.", "subject": "EVS", "topic": "Environment"},
    {"id": "evs_2",  "text": "Solar, wind, hydroelectric and geothermal are renewable energy. Coal and petroleum are non-renewable.", "subject": "EVS", "topic": "Energy"},
    {"id": "evs_3",  "text": "The water cycle includes evaporation, condensation, precipitation, and collection.", "subject": "EVS", "topic": "Water"},
    {"id": "evs_4",  "text": "Biodiversity refers to the variety of life on Earth including plants, animals and microorganisms.", "subject": "EVS", "topic": "Biodiversity"},
    {"id": "evs_5",  "text": "Acid rain is caused by sulphur dioxide and nitrogen oxides from factories reacting with water.", "subject": "EVS", "topic": "Pollution"},
    {"id": "evs_6",  "text": "The three Rs of environment are Reduce, Reuse, and Recycle to minimize waste.", "subject": "EVS", "topic": "Conservation"},
    {"id": "evs_7",  "text": "Food chain shows energy flow from producers to consumers. Plants are producers.", "subject": "EVS", "topic": "Ecosystem"},
    {"id": "geo_1",  "text": "India is the seventh largest country. It has 28 states and 8 union territories. Capital is New Delhi.", "subject": "Geography", "topic": "India"},
    {"id": "geo_2",  "text": "The Himalayas are the highest mountain range in India. They include Mount Everest.", "subject": "Geography", "topic": "India"},
    {"id": "geo_3",  "text": "Monsoon season brings heavy rainfall to India from June to September.", "subject": "Geography", "topic": "Climate"},
    {"id": "hist_1", "text": "India gained independence from British rule on August 15 1947. Mahatma Gandhi led the movement.", "subject": "History", "topic": "Independence"},
    {"id": "hist_2", "text": "The Indian Constitution came into effect on January 26 1950. Dr B R Ambedkar is its chief architect.", "subject": "History", "topic": "Constitution"},
]

def get_vector(text: str):
    words = text.lower().split()
    vec = np.zeros(128)
    for w in words:
        vec[hash(w) % 128] += 1.0
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()

def keyword_search(query: str, top_k: int = 3):
    query_words = set(query.lower().split())
    scored = []
    for chunk in NCERT_CHUNKS:
        chunk_words = set(chunk["text"].lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk["text"]))
    scored.sort(reverse=True)
    return [text for score, text in scored[:top_k] if score > 0]

# Initialize Endee
print("Initializing Endee Vector Database...")
endee_index = None
try:
    db = Endee("./endee_db")
    print("Endee methods: " + str([m for m in dir(db) if not m.startswith("_")]))
    
    try:
        endee_index = db.create_index("ncert", dimension=128)
        for chunk in NCERT_CHUNKS:
            vec = get_vector(chunk["text"])
            endee_index.insert(
                id=chunk["id"],
                vector=vec,
                metadata={"text": chunk["text"], "subject": chunk["subject"]}
            )
        print("Endee index created with " + str(len(NCERT_CHUNKS)) + " chunks")
    except Exception as e1:
        print("create_index failed: " + str(e1))
        try:
            for chunk in NCERT_CHUNKS:
                vec = get_vector(chunk["text"])
                db.insert(
                    id=chunk["id"],
                    vector=vec,
                    metadata={"text": chunk["text"], "subject": chunk["subject"]}
                )
            endee_index = db
            print("Endee insert method worked!")
        except Exception as e2:
            print("insert failed: " + str(e2))
            try:
                for chunk in NCERT_CHUNKS:
                    vec = get_vector(chunk["text"])
                    db.upsert(
                        id=chunk["id"],
                        vector=vec,
                        metadata={"text": chunk["text"], "subject": chunk["subject"]}
                    )
                endee_index = db
                print("Endee upsert method worked!")
            except Exception as e3:
                print("All Endee methods failed: " + str(e3))
                endee_index = None
except Exception as e:
    print("Endee init failed: " + str(e))
    endee_index = None

def semantic_search(query: str, top_k: int = 3):
    if endee_index is not None:
        try:
            query_vec = get_vector(query)
            results = endee_index.search(query_vec, top_k=top_k)
            chunks = []
            for r in results:
                if isinstance(r, dict):
                    meta = r.get("metadata", r)
                    text = meta.get("text", "")
                    if text:
                        chunks.append(text)
            if chunks:
                return chunks
        except Exception as e:
            print("Endee search error: " + str(e))
    return keyword_search(query, top_k)

class Query(BaseModel):
    question: str

class QuizRequest(BaseModel):
    subject: str
    grade: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def home():
    return {
        "message": "IncluPlayAI Backend Running!",
        "vector_db": "Endee",
        "ai_model": "Groq LLaMA 3.3 70B",
        "chunks": len(NCERT_CHUNKS),
        "endee_status": "connected" if endee_index else "fallback mode"
    }

@app.post("/ask")
async def ask_question(query: Query):
    try:
        chunks = semantic_search(query.question, top_k=3)
        context = "\n".join(chunks)

        if context:
            prompt = (
                "You are a friendly NCERT tutor for Indian school students Grades 6-10. "
                "Use this NCERT context to answer clearly in 2-3 simple sentences:\n\n"
                "Context:\n" + context + "\n\n"
                "Student Question: " + query.question
            )
        else:
            prompt = (
                "You are a friendly NCERT tutor for Indian school students Grades 6-10. "
                "Answer clearly in 2-3 simple sentences: " + query.question
            )

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
        return {
            "answer": answer,
            "rag_used": len(chunks) > 0,
            "sources_found": len(chunks),
            "vector_db": "Endee"
        }
    except Exception as e:
        return {"answer": "Error: " + str(e), "rag_used": False}

@app.post("/search")
async def search_knowledge(req: SearchRequest):
    try:
        chunks = semantic_search(req.query, top_k=req.top_k)
        return {
            "query": req.query,
            "results": chunks,
            "count": len(chunks),
            "vector_db": "Endee"
        }
    except Exception as e:
        return {"results": [], "error": str(e)}

@app.post("/quiz")
async def generate_quiz(req: QuizRequest):
    try:
        chunks = semantic_search(req.subject, top_k=3)
        context = "\n".join(chunks)
        content = (
            "Generate exactly 5 multiple choice questions for " + req.subject +
            " for " + req.grade + " NCERT students. "
            "Context: " + context + "\n\n"
            "Return ONLY a valid JSON array:\n"
            '[{"q": "question", "options": ["A","B","C","D"], "answer": "correct"}]'
        )
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
            return {"questions": questions, "subject": req.subject}
        return {"questions": []}
    except Exception as e:
        return {"questions": [], "error": str(e)}

@app.get("/db-stats")
def db_stats():
    return {
        "vector_db": "Endee",
        "total_chunks": len(NCERT_CHUNKS),
        "subjects": ["Science", "Mathematics", "Tamil", "EVS", "Geography", "History"],
        "endee_status": "connected" if endee_index else "fallback mode",
        "status": "healthy"
    }