# tests/smoke_retrieval.py
from __future__ import annotations

import os
from pathlib import Path
from importlib import resources

from smart_librarian.rag import build_or_load_collection, search


def _csv_from_package() -> Path:
    # Locate the CSV file bundled inside the smart_librarian/data package
    return resources.files("smart_librarian").joinpath("data/book_summaries_en.csv")


def main() -> None:
    """Simple smoke test for semantic search in ChromaDB."""
    # Use a local ChromaDB directory under tests/ so we don't pollute the main repo root
    test_chroma_dir = Path(__file__).resolve().parent / "chroma"
    os.environ.setdefault("CHROMA_DIR", str(test_chroma_dir))

    csv_path = _csv_from_package()
    col = build_or_load_collection(csv_path)
    print(f"Loaded {col.count()} documents.")

    query = "I want a book about friendship and magic"
    results = search(col, query, n_results=3)

    print("\nTop 3 results for:", query)
    for r in results:
        print("-", r["metadata"]["title"])


# ===== PyTest integration (runs with `pytest -q`) =====
def test_smoke_retrieval() -> None:
    # Call the same logic; if it fails, the test fails
    main()


if __name__ == "__main__":
    main()
