import streamlit as st
import os

from scraper import extract_text
from vector_store import create_vector_store, load_vector_store
from qa_chain import build_chain

st.set_page_config(page_title="Website Chatbot", layout="centered")
st.title("🌐 Website-Based Chatbot")

# URL input
url = st.text_input("Enter Website URL")

# Button to index website
if st.button("Index Website"):
    try:
        text, title = extract_text(url)

        if len(text.strip()) == 0:
            st.error("No supported content found on this website.")
        else:
            db = create_vector_store(text, {"source": url, "title": title})
            st.session_state.chain = build_chain(db)
            st.success("Website indexed successfully!")

    except Exception as e:
        st.error("Invalid or unreachable URL")

# Load existing vector DB if available
if "chain" not in st.session_state:
    db = load_vector_store()
    if db:
        st.session_state.chain = build_chain(db)

# Question input
if "chain" in st.session_state:
    question = st.text_input("Ask a question about the website")

    if question:
        result = st.session_state.chain({"question": question})
        answer = result["answer"]

        if answer.strip() == "":
            st.write("The answer is not available on the provided website.")
        else:
            st.write(answer)
