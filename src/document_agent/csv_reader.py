import csv 
from pathlib import Path

def read_csv(file_path:Path)->list[dict]:
    """Reads a csv file and returns its rows as dictionaries"""

    rows=[]
    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    )as file:

      reader=csv.DictReader(file,strict=True)   #Reads each row as a dictionary

      headers=next(reader,None)

      if not headers:
        raise ValueError("CSV file is empty or has no header")

      if any(not header.strip() for header in headers):
        raise ValueError("CSV contains an empty column name.")

      if len(headers)!=len(set(headers)):
        raise ValueError("Csv contains duplicate column names")

      for line_number, values in enumerate(reader,start=2):

        if len(values)!=len(headers):
          raise ValueError(
            f"Invalid number of columns at line {line_number}"
            f"Expected {len(headers)}, got {len(values)}"
          )
        rows.append(dict(zip(headers,values)))
    
    return rows