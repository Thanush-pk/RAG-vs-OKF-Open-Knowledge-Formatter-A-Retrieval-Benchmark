import requests
import numpy as np

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return np.array(response.json()["embedding"])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

sentences = [
    "The dog is sleeping",
    "The puppy is napping",
    "Stock prices fell today",
]

embeddings = [get_embedding(s) for s in sentences]

print("Shape of one embedding:", embeddings[0].shape)

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        score = cosine_similarity(embeddings[i], embeddings[j])
        print(f"'{sentences[i]}' vs '{sentences[j]}' -> similarity: {score:.4f}")