from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("✅ FAISS index loaded successfully!")

# Create retriever
retriever = vector_store.as_retriever()

# User query
query = "What is RAG?"

# NEW API usage
docs = retriever.invoke(query)

print("\n🔎 Retrieved Documents:\n")
for i, doc in enumerate(docs, start=1):
    print(f"{i}. {doc.page_content}")
