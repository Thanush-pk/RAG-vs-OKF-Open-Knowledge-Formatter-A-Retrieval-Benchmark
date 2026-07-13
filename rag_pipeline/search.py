import json
import faiss
import numpy as np
from build_index import get_embedding, INDEX_PATH, METADATA_PATH

def load_index_and_metadata():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def search(query, top_k=3):
    index, metadata = load_index_and_metadata()

    # Embed the query using get_embedding with the "search_query: " prefix
    query_vector = get_embedding(query, "search_query: ").astype("float32")
    
    # Normalize the query vector the same way we normalized during indexing
    # (faiss.normalize_L2 expects a 2D array, so reshape to 1 x dimension)
    query_vector = np.expand_dims(query_vector, axis=0)
    faiss.normalize_L2(query_vector)
    
    # Use index.search(query_vector, top_k) to get distances and indices
    distances, indices = index.search(query_vector, top_k)
    
    # For each returned index, look up metadata[index] and print/return
    # the source, section, and text, along with its similarity score
    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        match = metadata[idx]
        results.append((score, match))
        print(f"\nSimilarity Score: {score:.4f}")
        print(f"Source: {match['source']}")
        print(f"Section: {match['section']}")
        print("Text preview:")
        print(match['text'])
        print("-" * 50)
        
    return results

if __name__ == "__main__":
    query = input("Enter a question: ")
    search(query)
