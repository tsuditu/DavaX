# smart_librarian/utils.py
from importlib import resources
from pathlib import Path

def data_file(name: str) -> Path:
    """
    Return a real filesystem path to a data file bundled in
    smart_librarian/data (works in editable installs and wheels).
    """
    return resources.files("smart_librarian").joinpath(f"data/{name}")
