from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("Creating Vector Database...")

documents = [
    "Photosynthesis is the process by which green plants make their own food using sunlight, carbon dioxide, and water.",
    "Newton's First Law: An object at rest stays at rest unless acted upon by an external force.",
    "Jupiter is the largest planet in our solar system.",
    "Water boils at 100 degree Celsius at sea level.",
    "Matter has three states: Solid, Liquid, and Gas.",
    "Force equals mass times acceleration. This is Newton's Second Law.",
    "The human body has 206 bones in an adult.",
    "Chlorophyll is the green pigment in plants that absorbs sunlight for photosynthesis.",
]

text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
texts = text_splitter.create_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory="./data")

print("Vector Database Created Successfully!")
print(f"Total chunks stored: {len(texts)}")
