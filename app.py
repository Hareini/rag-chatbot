from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline

from transformers import pipeline

# 1️⃣ Load embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2️⃣ Load FAISS index
vector_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print("✅ FAISS index loaded")

# 3️⃣ Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 4️⃣ Load small LLM (CPU friendly)
pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_new_tokens=200
)

llm = HuggingFacePipeline(pipeline=pipe)

# 5️⃣ Ask a question
query = "What is robotics?"
docs = retriever.invoke(query)

print("\n🔎 Retrieved Context:\n")
for i, d in enumerate(docs, 1):
    print(f"{i}. {d.page_content[:300]}...\n")

# 6️⃣ Generate answer
context = "\n".join([d.page_content for d in docs])

prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

response = llm.invoke(prompt)

print("\n🤖 Final Answer:\n")
print(response)
