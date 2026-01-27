from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------- APP ----------------

app = FastAPI(title="Professional Website RAG Chatbot")


# ---------------- Schemas ----------------

class IngestWebsite(BaseModel):
    url: str


class Question(BaseModel):
    question: str
    style: Optional[str] = "Detailed"


# ---------------- Globals ----------------

VECTORSTORE = None

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------- Utils ----------------

def clean_text(text):
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_website_text(url):

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("Fetch error:", e)
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "table", "form"]):
        tag.decompose()

    paragraphs = soup.find_all("p")

    content = []

    for p in paragraphs:
        t = clean_text(p.get_text())
        if len(t) > 80:
            content.append(t)

    if not content:
        return None

    return "\n\n".join(content)


# ---------------- Helper (safe answer trimming) ----------------

def build_answer(text, max_length=450):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    final = ""
    for s in sentences:
        if len(final) + len(s) <= max_length:
            final += s + " "
        else:
            break

    return final.strip()


# ---------------- API Endpoints ----------------

@app.post("/ingest/website")
def ingest_website(data: IngestWebsite):
    global VECTORSTORE

    text = fetch_website_text(data.url)

    if text is None:
        return {
            "status": "success",
            "preview": "⚠️ Website blocked or no readable content found."
        }

    doc = Document(page_content=text)

    chunks = splitter.split_documents([doc])

    VECTORSTORE = FAISS.from_documents(chunks, embeddings)

    return {
        "status": "success",
        "preview": text[:600] + "..."
    }


@app.post("/ask")
def ask_question(q: Question):

    if VECTORSTORE is None:
        return {"answer": "Please ingest a website first."}

    results = VECTORSTORE.similarity_search_with_score(
        q.question,
        k=4
    )

    if not results:
        return {"answer": "Please ask questions related to the website content."}

    best_score = results[0][1]

    # Lower score = better match
    if best_score > 0.95:
        return {"answer": "Please ask questions related to the website content."}

    # Combine chunks
    context = " ".join(doc.page_content for doc, _ in results)

    focused_answer = build_answer(context)

    # -------- Styles --------

    if q.style == "Concise":
        return {"answer": build_answer(focused_answer, 180)}

    elif q.style == "Explain Like I'm 5":
        simple = focused_answer
        simple = simple.replace("administration", "office")
        simple = simple.replace("corporate", "company")
        simple = simple.replace("complex", "group of buildings")

        return {"answer": "Simply put: " + simple}

    else:
        return {"answer": focused_answer}


# ---------------- Health ----------------

@app.get("/")
def home():
    return {"status": "running"}
