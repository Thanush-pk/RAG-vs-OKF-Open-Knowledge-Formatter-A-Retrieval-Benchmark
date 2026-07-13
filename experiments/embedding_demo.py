from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# This downloads a small pre-trained model the first time (~90MB), then caches it locally
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "The dog is sleeping",
    "The puppy is napping",
    "Stock prices fell today",
]

embeddings = model.encode(sentences)

print("Shape of one embedding:", embeddings[0].shape)  # should print (384,)

# Compare similarity between each pair
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        score = cos_sim(embeddings[i], embeddings[j])
        print(f"'{sentences[i]}' vs '{sentences[j]}' -> similarity: {score.item():.4f}")