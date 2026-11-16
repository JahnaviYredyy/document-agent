import json
import re 
import shutil
from pathlib import Path

catalogue_path=Path("data/catalogue.json")
backup_path=Path("data/catalogue_backup.json")
shutil.copy2(catalogue_path,backup_path)
documents=json.loads(catalogue_path.read_text(encoding="utf-8"))

cleaned_documents=[]
seen_hashes=set()
seen_ids=set()

for document in documents:
    document_id=document.get("id")
    file_hash=document.get("sha256","")
    filename=document.get("original_name","")

    if filename=="malformed.csv":
        continue
    if not re.fullmatch(r"[a-fA-F0-9]{64}",file_hash):
        continue
    if document_id in seen_ids or file_hash in seen_hashes:
        continue

    cleaned_documents.append(document)
    seen_ids.add(document_id)
    seen_hashes.add(file_hash)

catalogue_path.write_text(
    json.dumps(cleaned_documents,indent=4),
    encoding="utf-8"
) 
print("Catalogue Cleanup completed")
print("Original records:",len(documents))
print("Remaining records:",len(cleaned_documents))
print("Backup saved at: ",backup_path)
