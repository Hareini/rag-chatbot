from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

print("📄 Loading PDF...")

pdf_path = "data/pdfs"

documents = []

for file in os.listdir(pdf_path):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_path, file))
        documents.extend(loader.load())

print(f"✅ Loaded {len(documents)} pages")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)
print(f"✂️ Created {len(chunks)} chunks")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local("faiss_index")
print("✅ FAISS index created from PDF")
