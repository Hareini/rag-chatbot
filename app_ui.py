import streamlit as st
from app import retriever, llm  # use your working app.py objects

st.title("📄 RAG QA Chatbot")

query = st.text_input("Ask a question:")

if query:
    # Use the correct method for your current retriever
    docs = retriever.invoke(query)

    st.subheader("Retrieved Documents:")
    for i, doc in enumerate(docs, 1):
        st.write(f"{i}. {doc.page_content[:500]}")  # show first 500 chars

    # Generate answer using LLM
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""
    answer = llm.invoke(prompt)
    st.subheader("Answer:")
    st.write(answer)
