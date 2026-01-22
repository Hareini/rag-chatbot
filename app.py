from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Load text
with open("data/sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Text loaded:")
print(text)

# 2. Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = text_splitter.split_text(text)

print("\nText chunks:")
for chunk in chunks:
    print("-", chunk)

# 3. Create embeddings (CORRECT way)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Store in FAISS
vector_store = FAISS.from_texts(chunks, embeddings)

print("\n✅ FAISS vector store created successfully!")


