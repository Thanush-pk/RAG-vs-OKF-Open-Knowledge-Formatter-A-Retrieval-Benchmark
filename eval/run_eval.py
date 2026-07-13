import sys
import os
import json
import time
import importlib.util
import contextlib
import io

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAG_DIR = os.path.join(PROJECT_ROOT, "rag_pipeline")
OKF_DIR = os.path.join(PROJECT_ROOT, "okf_pipeline")
QUESTIONS_PATH = os.path.join(PROJECT_ROOT, "eval", "golden_dataset", "questions.json")
RESULTS_PATH = os.path.join(PROJECT_ROOT, "eval", "results.json")


def load_module(module_name, file_path, extra_sys_path):
    """Load a .py file as a module under a specific name, adding its folder
    to sys.path first so its own internal imports (e.g. 'from search import ...')
    still resolve correctly."""
    if extra_sys_path not in sys.path:
        sys.path.insert(0, extra_sys_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_quietly(func, *args, **kwargs):
    """Run a function while suppressing its printed debug output,
    so the eval run's own progress log stays readable."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result


def main():
    rag_generate = load_module("rag_generate", os.path.join(RAG_DIR, "generate.py"), RAG_DIR)
    okf_generate = load_module("okf_generate", os.path.join(OKF_DIR, "generate.py"), OKF_DIR)

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []
    total = len(questions)

    for i, q in enumerate(questions):
        print(f"[{i+1}/{total}] {q['question']}")

        start = time.time()
        rag_answer = run_quietly(rag_generate.generate_answer, q["question"])
        rag_time = time.time() - start

        start = time.time()
        okf_answer = run_quietly(okf_generate.generate_answer, q["question"])
        okf_time = time.time() - start

        results.append({
            "id": q["id"],
            "type": q["type"],
            "question": q["question"],
            "expected_answer": q["expected_answer"],
            "expected_sources": q["expected_sources"],
            "rag_answer": rag_answer,
            "rag_time_seconds": round(rag_time, 2),
            "okf_answer": okf_answer,
            "okf_time_seconds": round(okf_time, 2)
        })

        print(f"   RAG ({rag_time:.1f}s): {rag_answer[:80]}...")
        print(f"   OKF ({okf_time:.1f}s): {okf_answer[:80]}...")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. Results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()