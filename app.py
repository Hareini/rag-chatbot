# app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8050"

st.set_page_config(page_title="Website RAG Chatbot", page_icon="🤖", layout="wide")

st.title("🌐 Website Ingestion RAG Chatbot")
st.write("Paste a website URL, ingest it, then ask questions!")

# ----- Session State -----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----- Step 1: Website Ingestion -----
st.subheader("1️⃣ Ingest Website")
url = st.text_input("Enter Website URL", placeholder="https://en.wikipedia.org/wiki/Artificial_intelligence")

if st.button("🚀 Ingest Website"):
    if not url:
        st.warning("Please enter a URL!")
    else:
        with st.spinner("Ingesting website..."):
            try:
                response = requests.post(f"{API_URL}/ingest/website", json={"url": url}, timeout=60)
                if response.status_code == 200:
                    st.success("✅ Website ingested successfully!")
                    st.text_area("Preview of Content", value=response.json().get("text_preview", ""), height=200)
                else:
                    st.error(f"❌ Failed: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🚫 Backend not running. Start FastAPI first.")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# ----- Step 2: Ask Questions -----
st.subheader("2️⃣ Ask Questions from Website")
question = st.text_input("Your Question", placeholder="What is Artificial Intelligence?")

if st.button("💬 Ask Question"):
    if not question:
        st.warning("Please type a question!")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=60)
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    context_preview = response.json()["retrieved_context"]

                    # Save in chat history
                    st.session_state.chat_history.append({"question": question, "answer": answer})

                    # Display chat history
                    for chat in reversed(st.session_state.chat_history):
                        st.markdown(f"**Q:** {chat['question']}")
                        st.markdown(f"**A:** {chat['answer']}\n---")

                    st.expander("📄 Retrieved Context Preview").write(context_preview)
                else:
                    st.error(f"❌ Failed: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🚫 Backend not running. Start FastAPI first.")
            except Exception as e:
                st.error(f"Error: {e}")
