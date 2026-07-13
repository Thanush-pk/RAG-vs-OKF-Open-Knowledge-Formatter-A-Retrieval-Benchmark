import os
import json
import requests
import numpy as np
import faiss

SOURCE_DIR = "data/source_docs"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"
INDEX_PATH = "rag_pipeline/faiss_index.bin"
METADATA_PATH = "rag_pipeline/chunks_metadata.json"


def get_embedding(text, prefix):
    prompt = prefix + text
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt}
    )
    return np.array(response.json()["embedding"])


def chunk_markdown(filepath):
    """Split a markdown file into chunks by '##' section headers."""
    filename = os.path.basename(filepath)
    doc_title = filename.replace(".md", "")  # e.g. "p99-latency-orders-api"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = []
    current_section = None
    current_lines = []

    def save_chunk(section, lines):
        text = "\n".join(lines).strip()
        # Enriched version used only for embedding - gives the model
        # the document/section context that the raw text alone might lack
        enriched_text = f"{doc_title} - {section}: {text}"
        chunks.append({
            "source": filename,
            "section": section,
            "text": text,              # clean version, shown to the user
            "embedding_text": enriched_text  # enriched version, used for embedding only
        })

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section is not None:
                save_chunk(current_section, current_lines)
            current_section = line.replace("## ", "").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_section is not None:
        save_chunk(current_section, current_lines)

    return chunks

def build_index():
    all_chunks = []
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".md"):
            chunks = chunk_markdown(os.path.join(SOURCE_DIR, filename))
            all_chunks.extend(chunks)

    print(f"Total chunks created: {len(all_chunks)}")

    embeddings = []
    for i, chunk in enumerate(all_chunks):
        vec = get_embedding(chunk["embedding_text"], "search_document: ")  # <-- changed
        embeddings.append(vec)
        print(f"Embedded chunk {i+1}/{len(all_chunks)}: {chunk['source']} - {chunk['section']}")

    embeddings_array = np.array(embeddings).astype("float32")

    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings_array)
    index.add(embeddings_array)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Index saved to {INDEX_PATH}")
    print(f"Metadata saved to {METADATA_PATH}")