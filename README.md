# Professional Website RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that ingests website content and allows users to chat with it using AI.  
Built using FastAPI for backend processing and Streamlit for frontend interface.

---

## Project Overview

This project allows users to:

- Ingest any public website URL
- Extract and clean content
- Convert content into vector embeddings
- Retrieve relevant information using semantic search
- Generate human-like responses using AI
- Manage chat history with delete and download options

---

## System Architecture

| Layer | Technology | Purpose |
|------|-----------|---------|
| Frontend | Streamlit | User interface for ingestion and chat |
| Backend API | FastAPI | Handles ingestion and question answering |
| Web Scraping | BeautifulSoup | Extract website content |
| Text Processing | LangChain | Split documents into chunks |
| Vector Store | FAISS | Store embeddings for retrieval |
| Embeddings | HuggingFace | Convert text to vectors |
| AI Model | BART (Transformers) | Summarize retrieved content |

---

## Workflow Architecture

| Step | Description |
|-----|------------|
| 1 | User inputs website URL |
| 2 | Backend scrapes and cleans website text |
| 3 | Text is split into chunks |
| 4 | Embeddings are generated |
| 5 | Stored in FAISS vector database |
| 6 | User asks question |
| 7 | Relevant chunks retrieved |
| 8 | AI summarizes and returns answer |

---

## Project Structure

| File | Description |
|-----|------------|
| api.py | FastAPI backend with RAG pipeline |
| app_ui.py | Streamlit user interface |
| requirements.txt | Python dependencies |
| README.md | Project documentation |

---

## Features

| Feature | Status |
|--------|-------|
| Website ingestion | Yes |
| RAG-based search | Yes |
| AI-generated answers | Yes |
| Answer styles | Yes |
| Chat history | Yes |
| Delete individual chats | Yes |
| Download chat | Yes |
| Error handling | Yes |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot

