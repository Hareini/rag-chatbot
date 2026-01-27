import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Website RAG Assistant",
    layout="centered"
)

# ---------------- Header ----------------

st.markdown(
    "<h1 style='text-align:center;'>Website RAG Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:gray;'>Ingest a website and interact with its content using AI-powered search</p>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- Session ----------------

if "chat" not in st.session_state:
    st.session_state.chat = []


# ---------------- Website Ingestion ----------------

st.subheader("Website Ingestion")

url = st.text_input("Enter Website URL", placeholder="https://example.com")

if st.button("Ingest Website", use_container_width=True):

    if not url:
        st.warning("Please enter a valid website URL")

    else:
        with st.spinner("Processing website content..."):

            try:
                response = requests.post(
                    f"{API_URL}/ingest/website",
                    json={"url": url},
                    timeout=30
                )

                data = response.json()

                st.success("Website successfully ingested")

                st.text_area(
                    "Extracted Content Preview",
                    data.get("preview", ""),
                    height=180
                )

            except:
                st.error("Backend service is not running")


st.divider()


# ---------------- Chat Section ----------------

st.subheader("Ask Questions")

question = st.text_input(
    "Enter your question",
    placeholder="Example: Where is the headquarters located?"
)

style = st.selectbox(
    "Response Style",
    [
        "Detailed Explanation",
        "Short Summary",
        "Simple Explanation"
    ]
)

if st.button("Submit Question", use_container_width=True):

    if not question:
        st.warning("Please enter a question")

    else:
        with st.spinner("Generating response..."):

            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question,
                        "style": style.replace(" Explanation", "").replace(" Summary", "").replace("Simple", "Explain Like I'm 5")
                    },
                    timeout=30
                )

                answer = response.json()["answer"]

                st.session_state.chat.append((question, answer))

            except:
                st.error("Unable to connect to backend service")


# ---------------- Chat Controls ----------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Clear All Conversations", use_container_width=True):
        st.session_state.chat = []
        st.success("Conversation history cleared")

with col2:
    if st.session_state.chat:

        chat_text = ""

        for i, (q, a) in enumerate(st.session_state.chat, 1):
            chat_text += f"Conversation {i}\nQuestion: {q}\nAnswer: {a}\n\n"

        st.download_button(
            "Download Conversation History",
            chat_text,
            "chat_history.txt",
            "text/plain",
            use_container_width=True
        )


# ---------------- Chat Display ----------------

st.divider()
st.subheader("Conversation History")

if not st.session_state.chat:
    st.info("No conversations yet")

for i, (q, a) in enumerate(st.session_state.chat):

    container = st.container(border=True)

    with container:
        st.markdown(f"**Question:** {q}")
        st.markdown(f"**Answer:** {a}")

        col_chat, col_delete = st.columns([8,2])

        with col_delete:
            if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                st.session_state.chat.pop(i)
                st.rerun()
