from document_agent.models import create_document
from document_agent.catalogue import save_document,load_catalogue

document=create_document(
name="company_policy.txt",
file_type="txt",
file_hash="abc1123",
size=2500,
stored_path="data/storage/company_policy.txt",
)
save_document(document)
print("Document saved ")
records=load_catalogue()
print("\nDocuments in catalogue")

for record in records:
    print(record["id"],record["original_name"])