
import argparse
from pathlib import Path

from document_agent.catalogue import load_catalogue
from document_agent.importer import import_folder
from document_agent.csv_reader import read_csv
from document_agent.pdf_reader import read_pdf


def list_documents() -> None:
    """Display all documents in the catalogue."""

    documents = load_catalogue()

    if not documents:
        print("No documents found.")
        return

    print(
        f"{'ID':36} "
        f"{'NAME':25} "
        f"{'TYPE':10} "
        f"{'SIZE(BYTES)':12} "
        f"{'STATUS':10}"
    )

    print("-" * 100)

    for document in documents:
        print(
            f"{document['id']:36} "
            f"{document['original_name'][:25]:25} "
            f"{document['file_type']:10} "
            f"{document['size_bytes']:<12} "
            f"{document['status']:10}"
        )


def inspect_document(document_id: str) -> None:
    """Display document metadata and a content preview."""

    documents = load_catalogue()

    document = next(
        (
            item for item in documents
            if item["id"] == document_id
        ),
        None,
    )

    if document is None:
        print("Document not found.")
        return

    print("\nDocument Details")
    print("-" * 40)

    print("ID:", document["id"])
    print("Name:", document["original_name"])
    print("Type:", document["file_type"])
    print("Size:", document["size_bytes"], "bytes")
    print("SHA256:", document["sha256"])
    print("Status:", document["status"])
    print("Imported at:", document["imported_at"])

    if document.get("page_count") is not None:
        print("Page count:", document["page_count"])

    file_path = Path(document["stored_path"])

    if not file_path.exists():
        print("\nStored document file not found.")
        return

    print("\nDocument Preview")
    print("-" * 40)

    file_type = document["file_type"]

    if file_type == "csv":
        rows = read_csv(file_path)

        if not rows:
            print("CSV file is empty.")
            return

        headers = list(rows[0].keys())

        print(" | ".join(headers))
        print("-" * 60)

        for row in rows[:5]:
            print(
                " | ".join(
                    str(row.get(header, ""))
                    for header in headers
                )
            )

        if len(rows) > 5:
            print("... Preview Limited.")

    elif file_type == "pdf":
        result = read_pdf(file_path)

        if not result["text"].strip():
            print("No extractable text; OCR may be needed.")
            return

        for page in result["pages"]:
            print(f"\n--- Page {page['page_number']} ---")

            if page["text"].strip():
                print(page["text"][:1000])
            else:
                print("No extractable text on this page.")

    else:
        content = file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        print(content[:500])

        if len(content) > 500:
            print("\n... Preview truncated.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Document Manager CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    import_parser = subparsers.add_parser(
        "import",
        help="Import documents from a folder",
    )
    import_parser.add_argument(
        "folder",
        help="Folder containing documents",
    )

    subparsers.add_parser(
        "list",
        help="List imported documents",
    )

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect a document",
    )
    inspect_parser.add_argument(
        "document_id",
        help="ID of the document",
    )

    args = parser.parse_args()

    if args.command == "import":
        import_folder(args.folder)

    elif args.command == "list":
        list_documents()

    elif args.command == "inspect":
        inspect_document(args.document_id)


if __name__ == "__main__":
    main()
