import json
from dataclasses import asdict
from pathlib import Path

from document_agent.models import Document


CATALOGUE_PATH = (Path(__file__).resolve().parents[2]/"data"/"catalogue.json")


def load_catalogue() -> list[dict]:
    """Load document records from the JSON catalogue."""

    if not CATALOGUE_PATH.exists():
        return []

    with CATALOGUE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)  #reads previously saved document records


def save_document(document: Document) -> None:
    """Add a document to the JSON catalogue."""

    records = load_catalogue()  

    records.append(asdict(document))

    CATALOGUE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CATALOGUE_PATH.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4) #writes records into json file
