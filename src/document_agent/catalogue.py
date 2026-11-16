import json
from dataclasses import asdict
from pathlib import Path

from document_agent.models import Document

#To stay in the projects data folder even when we run pythons script from different directories
CATALOGUE_PATH = (Path(__file__).resolve().parents[2]/"data"/"catalogue.json")


def load_catalogue() -> list[dict]:
    """Loads previously saved document records from the JSON catalogue."""

    if not CATALOGUE_PATH.exists():
        return []

    with CATALOGUE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)  #reads previously saved document and convers to python data


def save_document(document):
    """Saves only if its Id and content hash are new"""

    documents = load_catalogue()  

    for existing in documents:
        if existing["id"]==document.id:
            print("Document ID already exists. Skipping save")
            return
        if existing["sha256"]==document.sha256:
            print("Document content already exists.Skipping Save")
            return

    documents.append(asdict(document))

    CATALOGUE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CATALOGUE_PATH.open("w", encoding="utf-8") as file:
        json.dump(documents, file, indent=4) 
    
    print("Document saved to catalogue")
