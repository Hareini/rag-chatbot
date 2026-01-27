# Website RAG Assistant

A professional Retrieval-Augmented Generation (RAG) system that ingests website content and allows users to ask AI-powered questions through an interactive Streamlit interface.

The system extracts readable website text, converts it into vector embeddings, stores it in a FAISS vector database, and retrieves the most relevant content to answer user questions efficiently.

------------------------------------------------------------

## Project Features

┌──────────────────────────────────────────┐
│ ✓ Website content ingestion              │
│ ✓ Intelligent content cleaning           │
│ ✓ Chunk-based vector storage             │
│ ✓ AI-powered semantic search             │
│ ✓ Multiple response styles               │
│ ✓ Chat history management                │
│ ✓ Download conversation logs             │
│ ✓ FastAPI backend                        │
│ ✓ Streamlit frontend                     │
└──────────────────────────────────────────┘

------------------------------------------------------------

## High Level Architecture

┌────────────┐
│   User     │
└─────┬──────┘
      │
      ▼
┌───────────────┐
│ Streamlit UI  │
└─────┬─────────┘
      │ REST API
      ▼
┌───────────────┐
│ FastAPI App   │
└─────┬─────────┘
      │
      ▼
┌─────────────────────────┐
│ Website Scraper        │
│ (BeautifulSoup)        │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Text Splitter           │
│ (LangChain)             │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Embeddings Generator    │
│ (HuggingFace Model)     │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ FAISS Vector Database   │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Similarity Search       │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Context Builder         │
└─────┬──────────────────┘
      │
      ▼
┌─────────────────────────┐
│ Answer Generator        │
└─────────────────────────┘

------------------------------------------------------------

## Technology Stack

Frontend:
- Streamlit

Backend:
- FastAPI

AI & NLP:
- LangChain
- HuggingFace Sentence Transformers

Database:
- FAISS Vector Store

Web Scraping:
- BeautifulSoup4

Other:
- Requests
- Pydantic

------------------------------------------------------------

## Folder Structure

