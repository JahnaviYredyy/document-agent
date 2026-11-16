import os

from pathlib import Path
from document_agent.catalogue import load_catalogue, save_document
from document_agent.models import create_document
from document_agent.storage import calculate_hash, copy_to_storage
from document_agent.pdf_reader import read_pdf
from document_agent.csv_reader import read_csv

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".pdf"}


def import_folder(folder: str) -> None:
    """Import supported documents from a folder."""

    input_folder = Path(folder).resolve()

    if not input_folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not input_folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    records = load_catalogue()
    existing_hashes = {
        record["sha256"] for record in records
    }

    imported_count = 0

    for file_path in input_folder.rglob("*"):
        try:
            if not file_path.is_file():
                continue

            resolved_path = file_path.resolve()

            # Prevent importing files outside the input folder.
            if not resolved_path.is_relative_to(input_folder):
                print(f"Skipped unsafe path: {file_path}")
                continue

            extension = resolved_path.suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:
                print(f"Unsupported file: {file_path.name}")
                continue

            file_hash = calculate_hash(resolved_path)

            if file_path.suffix.lower() == ".csv":
                read_csv(resolved_path)

            if file_hash in existing_hashes:
                print(f"Duplicate skipped: {file_path.name}")
                continue
        

            page_count = None

            # Extract PDF information before importing.
            if extension == ".pdf":
                pdf_result = read_pdf(resolved_path)
                page_count = pdf_result["page_count"]

                if not pdf_result["text"].strip():
                    print(
                        f"No extractable text; OCR may be needed: "
                        f"{file_path.name}"
                    )
                elif pdf_result["empty_pages"]:
                    print(
                        f"Pages without extractable text "
                        f"({pdf_result['empty_pages']}): "
                        f"{file_path.name}"
                    )

            stored_path = copy_to_storage(
                resolved_path,
                file_hash
            )

            document = create_document(
                name=file_path.name,
                file_type=extension.lstrip("."),
                file_hash=file_hash,
                size=resolved_path.stat().st_size,
                stored_path=str(stored_path),
                page_count=page_count,
            )

            save_document(document)

            existing_hashes.add(file_hash)
            imported_count += 1

            print(f"Imported: {file_path.name}")

        except Exception as error:
            print(f"Failed to import {file_path.name}: {error}")

    print(f"\nImport completed. Total imported: {imported_count}")
