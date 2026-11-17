
import shutil

import pytest

import document_agent.importer as importer


def setup_importer(tmp_path, monkeypatch):
    # Create a temporary storage folder
    storage_dir = tmp_path / "storage"

    # Store imported documents in this temporary folder
    def copy_file(file_path, file_hash):
        destination = storage_dir / f"{file_hash}_{file_path.name}"
        storage_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, destination)
        return destination

    # Collect saved documents during testing
    saved_documents = []

    monkeypatch.setattr(importer, "load_catalogue", lambda: [])
    monkeypatch.setattr(importer, "copy_to_storage", copy_file)
    monkeypatch.setattr(
        importer,
        "create_document",
        lambda **kwargs: kwargs
    )
    monkeypatch.setattr(
        importer,
        "save_document",
        lambda document: saved_documents.append(document)
    )

    return saved_documents


def test_import_supported_file(tmp_path, monkeypatch):
    saved_documents = setup_importer(tmp_path, monkeypatch)

    # Create an input folder and a text file
    input_folder = tmp_path / "input"
    input_folder.mkdir()

    file_path = input_folder / "notes.txt"
    file_path.write_text("Hello Document Manager", encoding="utf-8")

    # Import the folder
    importer.import_folder(str(input_folder))

    # Check whether one document was imported
    assert len(saved_documents) == 1
    assert saved_documents[0]["name"] == "notes.txt"


def test_skip_duplicate_file(tmp_path, monkeypatch):
    saved_documents = setup_importer(tmp_path, monkeypatch)

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    file1 = input_folder / "first.txt"
    file2 = input_folder / "second.txt"

    # Both files have identical content
    file1.write_text("Same content", encoding="utf-8")
    file2.write_text("Same content", encoding="utf-8")

    importer.import_folder(str(input_folder))

    # Only one document should be imported
    assert len(saved_documents) == 1


def test_skip_unsupported_file(tmp_path, monkeypatch):
    saved_documents = setup_importer(tmp_path, monkeypatch)

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    # Create an unsupported image file
    file_path = input_folder / "photo.png"
    file_path.write_text("Not a real image", encoding="utf-8")

    importer.import_folder(str(input_folder))

    # Unsupported files should not be imported
    assert len(saved_documents) == 0


def test_continue_after_invalid_csv(tmp_path, monkeypatch):
    saved_documents = setup_importer(tmp_path, monkeypatch)

    input_folder = tmp_path / "input"
    input_folder.mkdir()

    # Create an invalid CSV file
    invalid_csv = input_folder / "invalid.csv"
    invalid_csv.write_text(
        "id,name\n001,Asha,Extra",
        encoding="utf-8"
    )

    # Create a valid text file
    valid_file = input_folder / "valid.txt"
    valid_file.write_text("Valid document", encoding="utf-8")

    # Import both files
    importer.import_folder(str(input_folder))

    # The valid file should still be imported
    assert len(saved_documents) == 1
    assert saved_documents[0]["name"] == "valid.txt"


def test_missing_folder_raises_error(tmp_path):
    missing_folder = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        importer.import_folder(str(missing_folder))
