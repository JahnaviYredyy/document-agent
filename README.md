# Python Document Manager

A command-line document management application built with Python. It allows users to import, store, list, and inspect documents in different formats while maintaining a persistent document catalogue and detecting duplicate files using SHA-256 hashing.

## Features

- **Document Import:** Import supported documents from a specified folder.
- **Supported Formats:** TXT, Markdown (MD), CSV, and PDF files.
- **Document Storage:** Copies imported documents into managed storage while preserving the original files.
- **Duplicate Detection:** Uses SHA-256 hashing to identify duplicate file contents.
- **Document Catalogue:** Stores document metadata in a JSON catalogue.
- **Document Listing:** Displays imported documents with their IDs, filenames, types, sizes, and statuses.
- **Document Inspection:** Displays document metadata and content previews.
- **CSV Processing:** Reads CSV files, preserves leading zeros, handles missing values, and validates malformed rows.
- **PDF Processing:** Extracts text, counts pages, and identifies pages without extractable text.
- **Error Handling:** Handles individual file import failures without stopping the entire batch.
- **Image-only PDF Detection:** Identifies PDFs without extractable text and indicates when OCR may be needed.

## Project Structure

```text
document-agent/
│
├── src/
│   └── document_agent/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── catalogue.py
│       ├── storage.py
│       ├── importer.py
│       │
│       └── readers/
│           ├── __init__.py
│           ├── csv_reader.py
│           └── pdf_reader.py
│
├── samples/
│   └── input/
│
├── exercises/
│
├── data/
│   ├── catalogue.json
│   └── storage/
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technologies Used

- **Python 3.13** – Main programming language.
- **uv** – Python project and dependency management.
- **argparse** – Command-line interface.
- **dataclasses** – Document data model.
- **hashlib** – SHA-256 hashing and duplicate detection.
- **shutil** – File copying.
- **JSON** – Persistent document catalogue.
- **csv** – CSV reading and validation.
- **pypdf** – PDF text extraction and page handling.
- **UUID** – Unique document identifiers.
- **datetime** – UTC import timestamps.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd document-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the application

Use the following commands from the project root.

## Available Commands

### Import documents

Import documents from a folder:

```bash
uv run docagent import samples/input
```

### List documents

Display all imported documents:

```bash
uv run docagent list
```

### Inspect a document

Use the document ID returned by the list command:

```bash
uv run docagent inspect <document_id>
```

The inspection displays document metadata and a preview of its contents.

## Document Processing

### CSV Files

The CSV reader:

- Preserves values such as employee IDs with leading zeros.
- Handles missing cell values.
- Retains duplicate rows.
- Detects empty and duplicate column names.
- Validates inconsistent row lengths.
- Handles malformed CSV input.

### PDF Files

The PDF reader:

- Extracts text from PDF pages.
- Calculates the total page count.
- Identifies pages without extractable text.
- Detects PDFs with no extractable text and reports that OCR may be needed.
- Handles corrupted PDF files through import error handling.

**Note:** OCR functionality is not implemented. Image-only PDFs are identified, but their text is not extracted.

## Storage and Duplicate Detection

Imported files are copied into:

```text
data/storage/
```

Document metadata is maintained in:

```text
data/catalogue.json
```

Each document receives:

- A unique UUID.
- A SHA-256 content hash.
- Original filename and file type.
- File size and storage path.
- Import status and UTC timestamp.
- PDF page count, when applicable.

The SHA-256 hash is used to detect duplicate file contents and prevent repeated imports.

## Development and Code Quality

The project uses Python development tools to maintain code quality.

Ruff:

```bash
uv run ruff check .
uv run ruff format --check .
```

Mypy:

```bash
uv run mypy
```

Automated tests with pytest are planned as part of the final verification process.

## Future Improvements

- Automated testing with pytest.
- Improved catalogue error handling.
- Stronger input and storage path validation.
- Symbolic link security checks.
- Additional file-handling edge-case tests.
- Improved documentation and validation.

## Author

Developed as part of a Python Foundations and Document Tools assignment.
