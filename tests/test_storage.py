
from document_agent.storage import calculate_hash, copy_to_storage


def test_calculate_hash(tmp_path):
    # Create a sample file
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello World", encoding="utf-8")

    # Calculate its hash
    result = calculate_hash(file_path)

    # Check the hash
    assert len(result) == 64


def test_same_content_same_hash(tmp_path):
    # Create two files with the same content
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("Hello", encoding="utf-8")
    file2.write_text("Hello", encoding="utf-8")

    # Calculate hashes
    hash1 = calculate_hash(file1)
    hash2 = calculate_hash(file2)

    # Both hashes should be equal
    assert hash1 == hash2


def test_different_content_different_hash(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("Hello", encoding="utf-8")
    file2.write_text("Goodbye", encoding="utf-8")

    hash1 = calculate_hash(file1)
    hash2 = calculate_hash(file2)

    # Hashes should be different
    assert hash1 != hash2


def test_copy_to_storage(tmp_path, monkeypatch):
    # Create an original file
    source_file = tmp_path / "sample.txt"
    source_file.write_text("Document testing", encoding="utf-8")

    # Create a temporary storage folder
    storage_dir = tmp_path / "storage"

    # Change the storage location for this test
    monkeypatch.setattr(
        "document_agent.storage.STORAGE_DIR",
        storage_dir
    )

    # Calculate hash and copy file
    file_hash = calculate_hash(source_file)
    stored_file = copy_to_storage(source_file, file_hash)

    # Check whether the file was copied
    assert stored_file.exists()

    # Check whether copied content is correct
    assert stored_file.read_text(encoding="utf-8") == "Document testing"
