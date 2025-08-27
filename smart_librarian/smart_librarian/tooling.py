# smart_librarian/tooling.py
from __future__ import annotations

import json
import os
from pathlib import Path

from smart_librarian.utils import data_file


def _default_json() -> Path:
    """
    Resolve the JSON file with full book summaries bundled in the package.
    If SUMMARIES_JSON is set in the environment, use that path instead.
    """
    override = os.environ.get("SUMMARIES_JSON")
    return Path(override) if override else data_file("book_summaries_full_en.json")


def get_summary_by_title(title: str) -> str:
    """
    Return the full summary for the given book title.
    If the title is not found, return a default message.
    """
    json_path = _default_json()
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(title, "No summary found for this title.")
