
from document_agent.catalogue import load_catalogue, save_document
from document_agent.models import Document


def create_sample_document():
    return Document(
        id="doc-001",
        original_name="sample.txt",
        file_type=".txt",
        sha256="a" * 64,
        size_bytes=100,
        stored_path="data/storage/sample.txt",
        status="success",
        imported_at="2026-11-17T10:00:00+00:00"
    )


def test_load_empty_catalogue(tmp_path, monkeypatch):
    # Use a temporary catalogue file
    catalogue_file = tmp_path / "catalogue.json"

    monkeypatch.setattr(
        "document_agent.catalogue.CATALOGUE_PATH",
        catalogue_file
    )

    # Load catalogue when no file exists
    documents = load_catalogue()

    # It should return an empty list
    assert documents == []


def test_save_document(tmp_path, monkeypatch):
    catalogue_file = tmp_path / "catalogue.json"

    monkeypatch.setattr(
        "document_agent.catalogue.CATALOGUE_PATH",
        catalogue_file
    )

    # Create a sample document
    document = create_sample_document()

    # Save the document
    save_document(document)

    # Check whether catalogue file was created
    assert catalogue_file.exists()

    # Load saved documents
    documents = load_catalogue()

    # Check whether the document was saved
    assert len(documents) == 1
    assert documents[0]["original_name"] == "sample.txt"


def test_duplicate_document_not_saved(tmp_path, monkeypatch):
    catalogue_file = tmp_path / "catalogue.json"

    monkeypatch.setattr(
        "document_agent.catalogue.CATALOGUE_PATH",
        catalogue_file
    )

    # Create two documents with the same content hash
    document1 = create_sample_document()
    document2 = create_sample_document()

    document2.id = "doc-002"
    document2.original_name = "another_name.txt"

    # Save both documents
    save_document(document1)
    save_document(document2)

    # Load the catalogue
    documents = load_catalogue()

    # Only one document should exist
    assert len(documents) == 1
