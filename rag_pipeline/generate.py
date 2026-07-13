import requests
from search import search

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
GENERATION_MODEL = "phi3:latest"

def build_prompt(question, chunks):
    """
    Combine retrieved chunks and the question into a single prompt string.
    Should instruct the model to answer ONLY using the given context,
    and to say so clearly if the context doesn't contain the answer.
    """
    context_str = ""
    for idx, chunk in enumerate(chunks):
        context_str += f"Context source: {chunk['source']} (Section: {chunk['section']})\n"
        context_str += f"Content:\n{chunk['text']}\n"
        context_str += "-" * 40 + "\n"
    
    prompt = (
        "You are a helpful assistant. Use ONLY the following retrieved context blocks to answer the question.\n"
        "If you do not know the answer or the context does not contain enough information, state clearly that "
        "you cannot answer the question based on the provided context. Do not use external knowledge or make up answers.\n\n"
        f"Context:\n{context_str}\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    return prompt

def generate_answer(question, top_k=3):
    results = search(question, top_k=top_k)  # reuse our existing search function
    chunks = [match for score, match in results]

    prompt = build_prompt(question, chunks)

    # POST to OLLAMA_GENERATE_URL with json={"model": GENERATION_MODEL, "prompt": prompt, "stream": False}
    response = requests.post(
        OLLAMA_GENERATE_URL,
        json={
            "model": GENERATION_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    
    # Extract the generated text from the response JSON (key is "response")
    response_json = response.json()
    
    # Return the generated answer
    return response_json.get("response", "")

if __name__ == "__main__":
    question = input("Enter a question: ")
    answer = generate_answer(question)
    print("\nAnswer:", answer)
