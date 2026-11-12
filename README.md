# Document Agent

## Project Overview

Document Agent is a Python-based command-line application designed to manage documents from a local folder.

The application will allow users to import documents, view the list of imported documents, and inspect individual documents through terminal commands.

This project is being developed as part of the Python Foundations and Document Tools assignment.

## Technologies Used

- **Python 3.13** – Main programming language
- **uv** – Python project and dependency management
- **argparse** – Command-line argument parsing
- **dataclasses** – Structured representation of document information
- **pathlib** – File and directory path handling

## Project Structure

```text
document-agent/
│
├── src/
│   └── document_agent/
│       ├── __init__.py
│       ├── cli.py
│       └── models.py
│
├── exercises/
│   └── document_example.py
│
├── tests/
├── samples/
│   └── input/
│
├── data/
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## Work Completed

### 1. Project Setup

- Created the Python project using `uv`.
- Configured project details and dependencies in `pyproject.toml`.
- Set up the source-code directory using the `src` layout.
- Configured a command-line entry point for the application.

### 2. Command-Line Interface (CLI)

Implemented the initial CLI structure using Python's `argparse` module.

The application currently supports three commands:

| Command | Purpose |
|---|---|
| `docagent import <folder>` | Accepts a folder path for document importing |
| `docagent list` | Lists documents |
| `docagent inspect <id>` | Accepts a document ID for inspection |

The commands currently demonstrate argument parsing and command execution. Their actual document-management functionality will be implemented in later stages.

### 3. Document Data Model

Created `models.py` to define the structure of a document using Python's `dataclass`.

The `Document` model contains the following fields:

- `id` – Unique document identifier
- `original_name` – Original document filename
- `file_type` – Document format
- `sha256` – Document content hash
- `size_bytes` – Document size in bytes
- `stored_path` – Location of the stored document
- `status` – Current document status
- `imported_at` – Document import timestamp
- `page_count` – Number of pages, when applicable

A `create_document()` function was also implemented to create and return a `Document` object.

### 4. Basic Python Exercise

Created `exercises/document_example.py` to test the document model.

The exercise demonstrates:

- Importing a function from another Python module.
- Passing values to a function.
- Creating a dataclass object.
- Accessing individual object attributes.
- Printing the complete document object and its properties.

## How to Run

### Run the CLI

Display available commands:

```powershell
uv run docagent --help
```

Try the import command:

```powershell
uv run docagent import samples/input/
```

Try the list command:

```powershell
uv run docagent list
```

Try the inspect command:

```powershell
uv run docagent inspect 1
```

### Run the Document Model Exercise

```powershell
uv run python exercises/document_example.py
```

## Current Progress

The initial project structure, CLI argument parsing, document data model, and basic Python exercise have been completed.

The next development stage is implementing document catalogue persistence and the actual document import, listing, and inspection functionality.
