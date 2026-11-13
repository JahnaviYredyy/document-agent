from pathlib import Path
from document_agent.storage import calculate_hash, copy_to_storage

file_path=Path("samples/company_policy.txt")
file_hash=calculate_hash(file_path)
print("File hash:", file_hash)
stored_path=copy_to_storage(file_path, file_hash)
print("File copied to:", stored_path)