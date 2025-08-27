# smart_librarian/main.py
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import List, Dict, Any

import click
from openai import OpenAI

from smart_librarian.rag import build_or_load_collection, search
from smart_librarian.tooling import get_summary_by_title
from smart_librarian.utils import data_file  # <-- helper to resolve data paths


# ===============================
# System prompt for the LLM
# ===============================
SYSTEM_PROMPT = """
You are Smart Librarian, a helpful assistant that recommends books based on user interests.
Rules:
- Use the provided candidate books (from RAG) to pick the best title.
- Reply conversationally in English.
- After choosing a title, CALL THE TOOL get_summary_by_title(title) to fetch the full summary.
- Then produce a final answer that contains:
  1) A short recommendation line with the chosen title and why it fits.
  2) 'Full summary:' followed by the tool's returned text.
If the user uses offensive language, politely refuse and ask for a constructive query instead.
"""


# ===============================
# OpenAI Tools specification
# ===============================
def build_tools_spec() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "get_summary_by_title",
                "description": "Return the full summary for an exact book title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Exact title of the book",
                        }
                    },
                    "required": ["title"],
                },
            },
        }
    ]


# ===============================
# Core LLM selection + summarization
# ===============================
def llm_select_and_summarize(query: str, candidates: List[Dict[str, Any]]) -> str:
    client = OpenAI()

    # Prepare RAG candidate context
    context_lines = [c["document"] for c in candidates]
    context = "\n\n".join(context_lines)

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"User request: {query}\n\nCandidate books (RAG):\n{context}"},
    ]

    # First call: let the model choose & possibly call the tool
    resp = client.chat.completions.create(
        model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
        messages=messages,
        tools=build_tools_spec(),
        tool_choice="auto",
        temperature=0.2,
    )

    msg = resp.choices[0].message
    messages.append(
        {
            "role": msg.role,
            "content": msg.content or "",
            "tool_calls": msg.tool_calls,
        }
    )

    # If the model called the tool, execute and append result
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            if call.function.name == "get_summary_by_title":
                args = json.loads(call.function.arguments or "{}")
                title = args.get("title", "")
                tool_result = get_summary_by_title(title)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": "get_summary_by_title",
                        "content": tool_result,
                    }
                )

        # Second call: final answer including tool result
        final = client.chat.completions.create(
            model=os.environ.get("CHAT_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.2,
        )
        return final.choices[0].message.content or ""

    # Fallback: no tool call
    return msg.content or "(No response)"


# ===============================
# CLI entrypoint
# ===============================
def _default_csv() -> Path:
    """Default CSV shipped with the package (works regardless of CWD)."""
    return data_file("book_summaries_en.csv")


@click.command()
@click.option(
    "--csv",
    "csv_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=_default_csv,
    show_default=True,
    help="Path to CSV with short summaries",
)
@click.option(
    "--persist",
    "persist_dir",
    default="chroma",
    show_default=True,
    help="ChromaDB persistence directory",
)
@click.option(
    "--topk",
    default=5,
    show_default=True,
    help="How many RAG candidates to pass to the LLM",
)
def cli(csv_path: Path, persist_dir: str, topk: int):
    """Run the Smart Librarian chatbot in a simple CLI loop."""
    os.environ.setdefault("CHROMA_DIR", persist_dir)

    col = build_or_load_collection(csv_path)

    click.echo("Smart Librarian is ready. Type your request (or 'exit' to quit):\n")
    while True:
        query = click.prompt("> ", type=str)
        if query.strip().lower() in {"exit", "quit"}:
            break

        # Basic bad language filter (demo only)
        banned = {"idiot", "stupid", "trash"}
        if any(b in query.lower() for b in banned):
            click.echo("Let's keep it respectful. Please rephrase your request.")
            continue

        candidates = search(col, query, n_results=topk)
        answer = llm_select_and_summarize(query, candidates)
        click.echo("\n" + answer + "\n")


if __name__ == "__main__":
    cli()
