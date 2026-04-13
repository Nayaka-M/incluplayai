import os
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

app = Flask(__name__)
# 1. FIX: Explicitly allow the origin of your Flutter app to prevent "Connection Failed"
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 Configuration
os.environ["GOOGLE_API_KEY"] = "AIzaSyC8IF7VRpzG8O_3srNoZ6iA9wXtdkKCMtE"
DB_PATH = "./chroma_db"

# Cleanup old DB
if os.path.exists(DB_PATH):
    try:
        shutil.rmtree(DB_PATH)
        print("🧹 Cleaned old vector database.")
    except Exception as e:
        print(f"⚠️ Could not delete DB: {e}")

# Stable 2026 Models
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", version="v1", temperature=0.7)

# --- PIPELINE ---
def create_retriever(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    loader = DirectoryLoader(folder_path, glob="./*.txt", loader_cls=TextLoader)
    docs = loader.load()
    
    if not docs:
        docs = [Document(page_content="Knowledge base initialized.")]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    return Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=os.path.basename(folder_path)
    ).as_retriever()

print("📦 Initializing Subject Experts...")
math_retriever = create_retriever('./data/math')
science_retriever = create_retriever('./data/science')
print("✅ All Experts Online!")

# --- API ROUTE ---
@app.route('/ask', methods=['POST'])
def ask_tutor():
    try:
        data = request.json
        # 2. FIX: Check for BOTH "message" and "query" to be compatible with Flutter
        query = data.get("message") or data.get("query") or ""
        
        if not query:
            return jsonify({"reply": "I didn't hear a question!", "response": "I didn't hear a question!"})

        # Socratic routing logic
        is_math = any(k in query.lower() for k in ['math', 'solve', 'x', '=', '+', '-', 'multiply'])
        subject = "MATH" if is_math else "SCIENCE"
        retriever = math_retriever if is_math else science_retriever
                
        template = "You are a Socratic {subject} tutor. Context: {context}. Question: {question} Hint:"
        prompt = ChatPromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough(), "subject": lambda x: subject} 
            | prompt | llm | StrOutputParser()
        )
        
        result = chain.invoke(query)
        
        # 3. FIX: Flutter is likely expecting "response", but code was sending "reply"
        return jsonify({
            "reply": result, 
            "response": result, 
            "subject": subject
        })

    except Exception as e:
        print(f"🔴 Server Error: {e}")
        return jsonify({"reply": "I'm having a glitch!", "response": "Technical glitch!", "error": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' is required for the app to see the server
    app.run(host='0.0.0.0', port=5000, debug=True)