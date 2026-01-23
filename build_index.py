from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load text file
with open("data/sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Text loaded")

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
chunks = splitter.split_text(text)

print("Text split into chunks")

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS index
vector_store = FAISS.from_texts(chunks, embeddings)

# Save FAISS index
vector_store.save_local("faiss_index")

print("✅ FAISS index created and saved")
