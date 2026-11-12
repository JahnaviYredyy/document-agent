import argparse

def main():
    parser=argparse.ArgumentParser(
        description="Document Agent -Manage your documents"
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

    args=parser.parse_args()

    if args.command =="import":
        print(f"Import command received:{args.folder}")
    elif args.command =="list":
        print("List command received")
    elif args.command =="inspect":
        print(f"Inspect command received:{args.document_id}")

if __name__=="__main__":
    main()
