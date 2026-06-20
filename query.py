import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# List available models
models = [
    m.name
    for m in genai.list_models()
    if "generateContent" in m.supported_generation_methods
]

print("Available models:")
for m in models:
    print(m)

# Use the first available model
model_name = models[0]

print(f"\nUsing model: {model_name}")

model = genai.GenerativeModel(model_name)

# Load document chunks
with open("../db/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

question = input("\nAsk your question: ")

context = ""

for chunk in chunks:
    if any(word.lower() in chunk["text"].lower()
           for word in question.split()):
        context += chunk["text"] + "\n"

if not context:
    print("No relevant information found.")
else:
    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}

Give a short and clear answer.
"""

    response = model.generate_content(prompt)

    print("\nAnswer:\n")
    print(response.text)