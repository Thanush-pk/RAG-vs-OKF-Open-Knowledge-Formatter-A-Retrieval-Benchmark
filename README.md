# RAG vs OKF: A Retrieval Benchmark

A hands-on comparison of two ways to give a language model access to a knowledge base: classic Retrieval-Augmented Generation (RAG) using embeddings and vector search, versus Google's Open Knowledge Format (OKF), a markdown-based knowledge representation released in mid-2026.

The goal was not to declare a winner. It was to build both approaches over the same source data, run them against the same question set, and see where each one actually breaks. The interesting results are the failures, not the successes — both systems answer easy questions fine, and they diverge in ways that aren't obvious until you measure them.

Everything here runs locally , using Ollama for both embeddings and generation.

---

## TL;DR of the findings

Across 18 questions (simple lookups, multi-hop questions, and deliberately unanswerable ones):

-  RAG scored 14/18 fully correct; OKF scored 13/18.  Close overall, but they failed on *different* questions, which is the point.
-  OKF was clearly better at dependency/relationship questions.  Following explicit links beats hoping the right chunks land in the top-k.
-  RAG was clearly better at "unanswerable" questions.  Counterintuitively, RAG's habit of always injecting *some* retrieved text kept the model grounded, so it declined to answer questions outside the knowledge base. OKF, when it found no matching concept, let the model fall back on its own training knowledge and answer anyway — which is the wrong behavior for a closed-book knowledge system.
-  OKF's "it's just file lookup, so it's faster" advantage disappears on multi-hop questions.  Once it follows links and pulls in several full documents, the prompt gets large and generation slows down — sometimes past RAG's time.

Neither approach dominates. The right choice depends on whether your users ask questions using your concepts' actual names, and whether false answers or missed answers are more costly for your use case.

---

## The setup

### Knowledge base

A synthetic but realistic internal knowledge base for a fictional "AI Platform Team" — 20 interlinked markdown documents covering:

- Services (5): auth-service, orders-api, agent-orchestrator, embedding-service, notification-service
-  Metrics  (5): p99 latency, agent success rate, throughput, auth failure rate, daily active agents
-  Runbooks  (5): deploy, rollback, incident response, key rotation, scaling
- Architecture/process docs  (5): system overview, agent lifecycle, on-call process, order data flow

The documents cross-reference each other the way real internal docs do (a runbook links to the metrics it monitors, a service links to its dependencies). This interlinking is what makes multi-hop questions meaningful.

### Path A — RAG

Standard retrieval pipeline:

1. Split each document into chunks by section header
2. Embed each chunk with `nomic-embed-text` (via Ollama)
3. Store vectors in a FAISS index (`IndexFlatIP` with L2-normalized vectors, so inner product = cosine similarity)
4. At query time: embed the question, retrieve the top 3 chunks, pass them to `phi3` for generation

### Path B — OKF

The same 20 documents, converted to OKF format (a YAML frontmatter block added on top of each — `type`, `title`, `description`, `tags`). Retrieval works structurally instead of by embedding similarity:

1. Try to match the question directly against a concept's name or title
2. If that fails, fall back to keyword overlap against each concept's title + description + tags
3. Follow markdown links from the matched concept one hop out, to pull in related concepts
4. Pass the matched concept(s) to `phi3` for generation

No embeddings, no vector store — just file parsing, string matching, and link traversal.

---

## Results

Scored as correct (✓), partial (~), or wrong (✗). Partial means the right answer was present but incomplete, buried, or hedged.

| # | Question type | RAG | OKF |
|---|---|:---:|:---:|
| 1 | current agent success rate | ✓ | ✓ |
| 2 | current p99 latency | ✓ | ✓ |
| 3 | current auth failure rate | ✓ | ✓ |
| 4 | daily active agents | ✓ | ✓ |
| 5 | embedding throughput target | ~ | ✓ |
| 6 | who owns auth-service | ✓ | ✓ |
| 7 | orders-api endpoints | ✓ | ✓ |
| 8 | orders-api dependencies + latency (multi-hop) | ✗ | ✓ |
| 9 | impact if embedding-service fails (multi-hop) | ~ | ✓ |
| 10 | high-latency incident procedure (multi-hop) | ✓ | ✓ |
| 11 | what to monitor after key rotation (multi-hop) | ✓ | ~ |
| 12 | incident escalation process | ✓ | ✓ |
| 13 | order lifecycle after creation (multi-hop) | ✓ | ✗ |
| 14 | rollback procedure + services | ✓ | ✓ |
| 15 | "what is AI?" (unanswerable) | ✓ | ✗ |
| 16 | "what's the weather?" (unanswerable) | ✓ | ✗ |
| 17 | "company revenue?" (unanswerable) | ✓ | ✓ |
| 18 | embedding throughput current value | ✓ | ✓ |

 Totals: RAG 14 ✓ / 2 ~ / 2 ✗ — OKF 13 ✓ / 1 ~ / 4 ✗ 

---

## What the failures actually tell us

### 1. OKF wins on relationship questions (Q8, Q9)

Question 8 — *"What services does orders-api depend on, and what is their current p99 latency?"* — is the clearest single result in the benchmark.

RAG failed it outright. Its top-3 chunks all came from the latency metric file, so the dependencies section of `orders-api` never made it into the context, and the model correctly said it couldn't find the dependencies. This is the fundamental limitation of top-k retrieval: relevant facts spread across multiple documents only make it into the answer if they all independently rank high enough, and there's no guarantee they will.

OKF answered it correctly by design. It matched the `orders-api` concept, followed its outbound links, and had the whole dependency structure available. Following explicit relationships is more reliable than hoping similarity search surfaces every needed piece.

### 2. RAG wins on unanswerable questions (Q15, Q16) — and the reason is counterintuitive

The knowledge base contains nothing about artificial intelligence or the weather. The correct behavior is to decline.

RAG declined correctly. Because it always retrieves *something* and puts it in the prompt, the model stayed anchored to "answer from the provided context only" and refused when the context was irrelevant.

OKF answered anyway — pulling definitions of AI and general knowledge about weather from the model's own training. When OKF's retriever found no matching concept, its prompt contained no grounding text to hold the model back, so the model reverted to being a general chatbot.

This is worth sitting with: RAG's least elegant property — that it force-feeds the model some chunk even when nothing's a great match — turned out to be an accidental safety feature. For a closed-book system where a confidently wrong answer is worse than "I don't know," this matters a lot. It's also fixable in OKF by explicitly instructing the model to decline when no concept is retrieved — but the default behavior, without that guard, is unsafe.

### 3. OKF's keyword matching is brittle where RAG's semantics are strong (Q13)

*"What happens to an order after it is created?"* is answered by the `data-flow-orders` document. But that question shares almost no literal words with the document's title, description, or tags — "order" is too common to be distinctive, and "data flow" never appears in the question. Both of OKF's matching strategies missed, and it returned nothing.

RAG handled it easily, because embeddings match on *meaning*, not shared words — "what happens to an order" is semantically close to a document describing an order's journey through the system, even with no vocabulary overlap.

This is the mirror image of finding #1. OKF's structural retrieval is precise when the question maps cleanly to a concept, and blind when it doesn't. RAG's semantic retrieval is fuzzier but degrades more gracefully.

### 4. The speed story is more nuanced than expected

For single-concept lookups, OKF's retrieval is effectively free — no embedding call, just file reads and string operations — while RAG pays for an embedding call on every query.

But that advantage inverts on multi-hop questions. When OKF follows links and pulls in four or five full documents, it hands the generation model a much larger prompt than RAG's three small chunks. Generation time scales with input size, so the heaviest multi-hop OKF answers were among the *slowest* in the whole run — slower than the equivalent RAG answers. "Just reading files is fast" is only true until you read a lot of files and feed them all to the model.

---

## A retrieval bug worth documenting

An early version of the RAG pipeline consistently failed to retrieve metric values. Asking for the current value of a metric returned everything *except* the number.

The cause: metric values were stored as their own chunks with almost no text — a chunk might contain just `94.2%`. A bare number carries almost no semantic signal for an embedding model, so it never ranked highly against a natural-language question, even though it was the exact answer.

The fix was to prepend each chunk's document title and section name to the text *before* embedding it — so `94.2%` becomes `agent-success-rate - Current Value: 94.2%` for embedding purposes, while the clean version is still what gets shown and passed to the model. Retrieval of numeric facts went from failing to reliable. This is a generally useful technique: sparse or numeric chunks need surrounding context baked into the embedded text, or they become invisible to retrieval.

---

## Honest limitations

-  Small scale.  20 documents and 18 questions is a demonstration, not a production benchmark. Real knowledge bases are orders of magnitude larger, and some of these findings (especially around speed and top-k coverage) would shift at scale.
-  Small local model.  `phi3` (3.8B) is the generation model, chosen to keep everything free and local. It occasionally truncates multi-item lists and, in a few answers, produced a stray "my training data goes up to..." disclaimer even when the answer was in front of it. A larger model would clean up some of the "partial" scores, but the *retrieval* differences between RAG and OKF would remain.
-  Manual scoring.  Answers were scored by hand against known-correct reference answers. The harness is structured so an automated judge (a stronger model scoring each answer) can be dropped in later without changing the rest of the pipeline.
-  OKF's matching is deliberately simple.  A production OKF system would likely add an embedding step just for *concept selection* — using semantics to pick which concept to open, then using OKF's structure to read and traverse it. That hybrid would likely fix the Q13-style failures while keeping the multi-hop advantages.

---

## Takeaway

If your users ask questions using the names of things in your system, and missing an answer is safer than inventing one, OKF's structural approach is precise, transparent, and cheap. If your users ask in their own words and you need graceful handling of vague or off-topic questions, RAG's semantic retrieval is more forgiving. The strongest system is probably a hybrid: semantic retrieval to find the right concept, structural traversal to read it and its neighbors.

The broader lesson from building both: retrieval quality, not model quality, decided most of these outcomes. Nearly every wrong answer traced back to the *wrong documents being retrieved*, not the model mishandling the right ones.

---

## Running it yourself

 Requirements:  Python 3.10+, [Ollama](https://ollama.com/) installed and running.

```bash
# Pull the models
ollama pull nomic-embed-text
ollama pull phi3

# Install dependencies
pip install -r requirements.txt

# Build the RAG index
python rag_pipeline/build_index.py

# Ask a single question through either pipeline
python rag_pipeline/generate.py
python okf_pipeline/generate.py

# Run the full evaluation across both pipelines
python eval/run_eval.py
```

## Project structure

```
.
├── data/
│   ├── source_docs/      # 20 plain-markdown docs (RAG source)
│   └── okf_bundle/       # same 20 docs in OKF format (frontmatter added)
├── rag_pipeline/         # chunking, embedding, FAISS index, retrieval, generation
├── okf_pipeline/         # concept parsing, keyword/link retrieval, generation
├── eval/
│   ├── golden_dataset/   # 18 question/answer pairs with expected sources
│   ├── run_eval.py       # runs all questions through both pipelines
│   └── results.json      # captured answers + timings
└── README.md
```
