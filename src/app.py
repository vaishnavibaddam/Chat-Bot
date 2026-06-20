import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

with open("../db/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

st.title("📄 Document Question Answering Bot")

question = st.text_input("Ask a question about your document")

if question:

    context = ""

    for chunk in chunks:
        if any(word.lower() in chunk["text"].lower()
               for word in question.split()):
            context += chunk["text"] + "\n"

    if context:

        prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Give a short and clear answer.
"""

        response = model.generate_content(prompt)

        st.subheader("Answer")
        st.write(response.text)

    else:
        st.warning("No relevant information found.")