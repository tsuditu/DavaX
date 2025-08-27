# smart_librarian/rag.py
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


def _persist_dir() -> str:
    """
    Return the Chroma persistence directory.
    Read from env at *runtime* so callers can set CHROMA_DIR before calling.
    """
    return os.environ.get("CHROMA_DIR", "chroma")


def get_chroma_client() -> chromadb.PersistentClient:
    """Create and return a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=_persist_dir())


def build_or_load_collection(
    csv_path: str | Path,
    collection_name: str = "book_summaries",
):
    """
    Build or load a ChromaDB collection using OpenAI embeddings.
    If the collection is empty, populate it with documents from the CSV dataset.

    Parameters
    ----------
    csv_path : str | Path
        Path to the CSV file containing at least columns: 'title', 'short_summary'.
    collection_name : str
        Name of the Chroma collection to create or load.
    """
    client = get_chroma_client()

    embedder = OpenAIEmbeddingFunction(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
    )

    col = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedder,
    )

    # Populate only if empty
    if col.count() == 0:
        csv_path = Path(csv_path)
        df = pd.read_csv(csv_path)

        # Basic validation
        missing = {"title", "short_summary"} - set(df.columns.str.lower())
        # If columns are capitalized differently, normalize access:
        title_col = next((c for c in df.columns if c.lower() == "title"), None)
        short_col = next((c for c in df.columns if c.lower() == "short_summary"), None)
        if not title_col or not short_col:
            raise ValueError(
                "CSV must contain 'title' and 'short_summary' columns "
                f"(found: {list(df.columns)})"
            )

        docs: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        ids: List[str] = []

        for i, row in df.iterrows():
            title = str(row[title_col])
            short = str(row[short_col])
            docs.append(f"Title: {title}\nSummary: {short}")
            metadatas.append({"title": title})
            ids.append(f"book-{i}")

        if docs:
            col.add(documents=docs, metadatas=metadatas, ids=ids)

    return col


def search(col, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Perform a semantic search in the collection.
    Returns a list of matching documents with metadata.
    """
    res = col.query(query_texts=[query], n_results=n_results)
    items: List[Dict[str, Any]] = []

    # Defensive: Chroma returns lists-of-lists
    ids = res.get("ids", [[]])[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0] if "distances" in res else [None] * len(ids)

    for i in range(len(ids)):
        items.append(
            {
                "id": ids[i],
                "document": docs[i],
                "metadata": metas[i],
                "distance": dists[i],
            }
        )
    return items
