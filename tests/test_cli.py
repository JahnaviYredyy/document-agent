
import document_agent.cli as cli


def test_list_empty_documents(monkeypatch, capsys):
    # Pretend the catalogue is empty
    monkeypatch.setattr(cli, "load_catalogue", lambda: [])

    # Run the list command
    cli.list_documents()

    # Capture printed output
    output = capsys.readouterr().out

    assert "No documents found." in output


def test_list_documents(monkeypatch, capsys):
    # Create a sample catalogue record
    documents = [
        {
            "id": "doc-001",
            "original_name": "notes.txt",
            "file_type": "txt",
            "size_bytes": 100,
            "status": "success"
        }
    ]

    monkeypatch.setattr(
        cli,
        "load_catalogue",
        lambda: documents
    )

    cli.list_documents()

    output = capsys.readouterr().out

    # Check whether the document name appears
    assert "notes.txt" in output
    assert "doc-001" in output


def test_inspect_missing_document(monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_catalogue", lambda: [])

    cli.inspect_document("wrong-id")

    output = capsys.readouterr().out

    assert "Document not found." in output


def test_import_command(monkeypatch):
    # Track whether import_folder was called
    called = []

    def fake_import_folder(folder):
        called.append(folder)

    monkeypatch.setattr(
        cli,
        "import_folder",
        fake_import_folder
    )

    # Provide command-line arguments
    monkeypatch.setattr(
        "sys.argv",
        ["docagent", "import", "samples"]
    )

    # Run the CLI
    cli.main()

    # Check whether the correct folder was passed
    assert called == ["samples"]
