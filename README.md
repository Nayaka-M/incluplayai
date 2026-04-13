## 🔍 How Endee is Used

Endee is used as the vector database to store and search NCERT educational content:

1. **Indexing** — 25+ NCERT knowledge chunks (Science, Math, Tamil, EVS) are embedded and stored in Endee on startup
2. **Semantic Search** — When a student asks a question, the query is embedded and searched against Endee to find the most relevant NCERT content
3. **RAG Pipeline** — Retrieved chunks are passed as context to Groq LLM for accurate, syllabus-grounded answers
4. **Quiz Generation** — Subject-relevant NCERT chunks are retrieved from Endee and used as context for Groq to generate better quiz questions

## ✨ Features

- 🤖 **AI Chat Tutor** — Ask any NCERT question, get RAG-powered answers
- 📝 **AI Quiz Generator** — Fresh Groq-generated questions every session
- 📊 **Real Progress Tracking** — Subject-wise progress bars updated after each quiz
- 🏆 **Gamification** — Points, streaks, quiz completion tracking
- 🌐 **Multilingual UI** — English, Tamil, Hindi support
- 📚 **4 Subjects** — Mathematics, Science, Tamil, EVS

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Flutter (Dart) |
| Backend | FastAPI (Python) |
| Vector DB | **Endee** |
| LLM | Groq (llama-3.3-70b-versatile) |
| State Management | Riverpod |

## 🚀 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Nayaka-M/incluplayai.git
cd incluplayai
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Flutter setup
```bash
cd ..
flutter pub get
flutter run -d chrome
```

### 4. Environment
Add your Groq API key in `backend/main.py`:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```

## 📁 Project Structure

## 🔗 Endee

This project uses [Endee](https://github.com/endee-io/endee) as the vector database for semantic search and RAG over NCERT educational content.


includuplay_edu/
├── lib/
│   ├── features/
│   │   ├── auth/          # Login screen
│   │   ├── dashboard/     # Main dashboard
│   │   ├── chat/          # AI Chat screen
│   │   ├── subjects/      # Math, Science, Tamil, EVS
│   │   ├── gamification/  # Points and streaks
│   │   └── history/       # Score history
│   └── core/
│       └── api/           # AI Tutor service
├── backend/
│   ├── main.py            # FastAPI + Endee + Groq
│   ├── requirements.txt
│   └── .env.example
└── README.md