from pathlib import Path

from document_agent.csv_reader import read_csv

file_path=Path("samples/employees.csv")
rows=read_csv(file_path)
print("CSV contents:\n")
for row in rows:
    print(row)

print("\nTotal rows:",len(rows))