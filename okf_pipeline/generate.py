import requests
from okf_search import search_with_hops

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
GENERATION_MODEL = "phi3:latest"


def build_prompt(question, retrieved_concepts):
    if not retrieved_concepts:
        context_str = "(No matching concept was found in the knowledge base.)"
    else:
        parts = []
        for key, concept in retrieved_concepts:
            fm = concept["frontmatter"]
            parts.append(
                f"--- Concept: {fm.get('title', key)} (Type: {fm.get('type', '')}) ---\n"
                f"{concept['body']}"
            )
        context_str = "\n\n".join(parts)

    prompt = (
            "You are a helpful assistant. Use ONLY the following retrieved concepts to answer the question.\n"
"The concepts may reference each other; use all of them together if needed to fully answer.\n"
"Answer completely — if the question has multiple parts, address every part explicitly.\n"
"If the concepts do not contain enough information, state clearly that you cannot answer.\n\n"
        f"Context:\n{context_str}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    return prompt


def generate_answer(question, max_hops=1):
    retrieved = search_with_hops(question, max_hops=max_hops)
    prompt = build_prompt(question, retrieved)

    response = requests.post(
        OLLAMA_GENERATE_URL,
        json={"model": GENERATION_MODEL, "prompt": prompt, "stream": False}
    )
    response.raise_for_status()
    return response.json().get("response", "")


if __name__ == "__main__":
    question = input("Enter a question: ")
    answer = generate_answer(question)
    print("\nAnswer:", answer)