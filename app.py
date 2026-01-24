from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline

# 1️⃣ Load embeddings (same as build_index.py)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2️⃣ Load FAISS index
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("✅ FAISS index loaded successfully!")

# 3️⃣ Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 4️⃣ Load local LLM (Flan-T5)
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=200
)

# 5️⃣ Ask question
query = "What is RAG?"

docs = retriever.invoke(query)

context = "\n".join([doc.page_content for doc in docs])

prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

# 6️⃣ Generate answer
response = llm(prompt)

print("\n🤖 Answer:")
print(response[0]["generated_text"])
