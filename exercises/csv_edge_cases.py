import csv
from pathlib import Path
from document_agent.csv_reader import read_csv

file_path=Path("samples/malformed.csv")

try:
    rows=read_csv(file_path)
    print(rows)

except(ValueError,csv.Error)as error:
    print("CSV Reading failed:",error)