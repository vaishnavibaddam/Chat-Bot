from pypdf import PdfReader
import os
import json


def extract_pdf(file_path):
    pages = []

    reader = PdfReader(file_path)

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append({
                "text": text,
                "source": os.path.basename(file_path),
                "page": i + 1
            })

    return pages


def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        text = page["text"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunks.append({
                "text": text[start:end],
                "source": page["source"],
                "page": page["page"]
            })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    folder = "../data"

    all_chunks = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)

            pages = extract_pdf(path)

            chunks = chunk_text(pages)

            all_chunks.extend(chunks)

            print(f"Processed: {file}")

    with open("../db/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)

    print("Chunks saved successfully.")