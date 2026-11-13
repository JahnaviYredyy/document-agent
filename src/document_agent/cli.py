import argparse

from pathlib import Path
from document_agent.importer import import_folder
from document_agent.catalogue import load_catalogue

def main():
    parser=argparse.ArgumentParser(
        description="Document Management -CLI"
        )

    subparsers=parser.add_subparsers(
        dest="command",
        required=True
    )

    #Import command
    import_parser=subparsers.add_parser(
        "import",
        help="Import documents from a folder"
    )
    import_parser.add_argument("folder",help="Folder containing documents")

    #List command
    subparsers.add_parser(
        "list",
        help="List Imported documents"
    )
    
    # Inspect command
    inspect_parser = subparsers.add_parser(
        "inspect",
        help="Inspect a document"
    )
    inspect_parser.add_argument("document_id", help="Document ID")

    args=parser.parse_args() #Reads the arguments entered in the terminal and matches them against commands we defined

    if args.command =="import":
        import_folder(args.folder)

    elif args.command =="list":
        documents=load_catalogue()

        if not documents:
            print("No documents found")
            return
        print("\nDocuments in catalogue:\n")

        print(
            f"{'ID':<38}"
            f"{'NAME':<25}"
            f"{'TYPE':<10}"
            f"{'SIZE(BYTES)':<15}"
            f"{'STATUS'}"
        )
        print("-"*105)

        for document in documents:
            print(
                f"{document['id']:<38}"
                f"{document['original_name']:<25}"
                f"{document['file_type']:<10}"
                f"{document['size_bytes']:<15}"
                f"{document['status']}"
            )

    elif args.command =="inspect":
        documents = load_catalogue()

        document=next(
            (
                item for item in documents
                if item["id"] == args.document_id
            ),
            None
        )
        if document is None:
            print("Document not found.")
            return

        print("\nDocument Details")
        print("-" * 40)

        print("ID:",document["id"])
        print("Name:",document["original_name"])
        print("Type:",document["file_type"])
        print("Size:",document["size_bytes"],"bytes")
        print("SHA-256:",document["sha256"])
        print("Status:",document["status"])
        print("Imported at:",document["imported_at"])
        print("Stored path:",document["stored_path"])

        print("\nContent Preview")
        print("-" * 40)

        file_path=Path(document["stored_path"])

        if file_path.exists():
            content=file_path.read_text(
                encoding="utf-8",
                errors="replace"
            )

            print(comtent[:500])

            if len(content)>500:
                print("\n.. Preview truncated.")
        else:
            print("Stored document file not found.")
        
if __name__=="__main__":
    main()
