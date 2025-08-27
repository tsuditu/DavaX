import os
import click
from pathlib import Path
from importlib import resources
from smart_librarian.rag import build_or_load_collection


def default_csv_path() -> Path:
    # access the file included in the package
    return resources.files("smart_librarian").joinpath("data/book_summaries_en.csv")


@click.command()
@click.option(
    "--csv",
    "csv_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=default_csv_path,
    show_default=True,
    help="Path to the dataset CSV file",
)
@click.option(
    "--persist",
    default="chroma",
    show_default=True,
    help="Path where ChromaDB will persist the index",
)
def main(csv_path: Path, persist: str):
    """Build or load the ChromaDB collection and persist it."""
    os.environ.setdefault("CHROMA_DIR", persist)
    col = build_or_load_collection(csv_path)
    print(f"Collection '{col.name}' ready with {col.count()} docs at {persist}")


if __name__ == "__main__":
    main()
