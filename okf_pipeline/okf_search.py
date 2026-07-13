import os
import re

OKF_DIR = "data/OKF_bundle"

STOPWORDS = {"the", "is", "are", "a", "an", "how", "what", "does", "do",
             "for", "to", "of", "in", "on", "and", "or", "team", "platform"}


def load_concepts():
    """
    Read every .md file in OKF_DIR.
    For each file, parse out the frontmatter (as a dict) and the body.
    Return a dict like: { "auth-service": {"frontmatter": {...}, "body": "..."} }
    """
    concepts = {}
    if not os.path.exists(OKF_DIR):
        return concepts

    for filename in os.listdir(OKF_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(OKF_DIR, filename)
            concept_id = filename.replace(".md", "")

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm_text = parts[1]
                body_text = parts[2].strip()

                frontmatter = {}
                for line in fm_text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if ":" in line:
                        key, val = line.split(":", 1)
                        key = key.strip()
                        val = val.strip()
                        if val.startswith("[") and val.endswith("]"):
                            val = [item.strip() for item in val[1:-1].split(",") if item.strip()]
                        frontmatter[key] = val

                concepts[concept_id] = {
                    "frontmatter": frontmatter,
                    "body": body_text
                }
    return concepts


def tokenize(text):
    """Lowercase, extract words, strip stopwords, return a set."""
    words = re.findall(r'\b\w+\b', text.lower())
    return {w for w in words if w not in STOPWORDS}


def exact_match(question, concepts):
    """Fast path: check if concept filename or title appears literally in the question."""
    q_lower = question.lower()

    for key, concept in concepts.items():
        key_lower = key.lower()
        title = concept["frontmatter"].get("title", "")
        title_lower = title.lower() if isinstance(title, str) else ""

        if key_lower in q_lower or (title_lower and title_lower in q_lower):
            return key

    for key in concepts:
        key_spaced = key.replace("-", " ").replace("_", " ").lower()
        if key_spaced in q_lower:
            return key

    return None


def keyword_overlap_match(question, concepts, min_overlap=2):
    """
    Fallback: score each concept by word overlap between the question
    and the concept's title + description + tags. Return the best match
    if its score meets the minimum threshold.
    """
    question_words = tokenize(question)
    best_key = None
    best_score = 0

    for key, concept in concepts.items():
        fm = concept["frontmatter"]
        title = fm.get("title", "")
        description = fm.get("description", "")
        tags = fm.get("tags", [])
        tags_str = " ".join(tags) if isinstance(tags, list) else str(tags)

        searchable_text = f"{title} {description} {tags_str}"
        concept_words = tokenize(searchable_text)

        overlap = len(question_words & concept_words)

        if overlap > best_score:
            best_score = overlap
            best_key = key

    if best_score >= min_overlap:
        return best_key
    return None


def find_matching_concept(question, concepts):
    """Try exact match first (fast path), fall back to keyword overlap."""
    match = exact_match(question, concepts)
    if match is not None:
        return match, "exact"

    match = keyword_overlap_match(question, concepts)
    if match is not None:
        return match, "keyword_overlap"

    return None, None


def extract_linked_concepts(body, concepts):
    """
    Find all markdown links like [text](target.md) in the body,
    resolve them to concept IDs that actually exist in our concepts dict,
    and return the list of matched concept dicts (excluding duplicates).
    """
    # Matches [anything](something.md), capturing the filename part
    link_pattern = r'\[([^\]]+)\]\(([^)]+?)\.md\)'
    matches = re.findall(link_pattern, body)

    linked_ids = []
    for _, target in matches:
        # target might be like "p99-latency-orders-api" or "./p99-latency-orders-api"
        concept_id = target.strip().lstrip("./")
        if concept_id in concepts and concept_id not in linked_ids:
            linked_ids.append(concept_id)

    return linked_ids


def search_with_hops(question, max_hops=1):
    """
    Find the best-matching concept, then follow its outbound links
    up to max_hops levels deep, collecting all visited concepts.
    Returns a list of (concept_id, concept_dict) tuples:
    the primary match first, then linked concepts.
    """
    concepts = load_concepts()
    match_key, match_type = find_matching_concept(question, concepts)

    if match_key is None:
        print("No matching concept found.")
        return []

    visited = [match_key]
    result = [(match_key, concepts[match_key])]

    frontier = [match_key]
    for hop in range(max_hops):
        next_frontier = []
        for key in frontier:
            linked_ids = extract_linked_concepts(concepts[key]["body"], concepts)
            for linked_id in linked_ids:
                if linked_id not in visited:
                    visited.append(linked_id)
                    result.append((linked_id, concepts[linked_id]))
                    next_frontier.append(linked_id)
        frontier = next_frontier

    print(f"\nPrimary match: {match_key} (via {match_type})")
    print(f"Total concepts retrieved (including linked): {len(result)}")
    for key, _ in result:
        print(f"  - {key}")

    return result


def search(question):
    concepts = load_concepts()
    match_key, match_type = find_matching_concept(question, concepts)

    if match_key is None:
        print("No matching concept found.")
        return None

    concept = concepts[match_key]
    print(f"\nMatched concept: {match_key} (via {match_type})")
    print(f"Type: {concept['frontmatter'].get('type')}")
    print(f"Body:\n{concept['body']}")
    return concept


if __name__ == "__main__":
    question = input("Enter a question: ")
    search(question)