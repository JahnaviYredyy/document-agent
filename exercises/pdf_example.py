from pathlib import Path
from document_agent.pdf_reader import read_pdf

file_path=Path("samples/sample.pdf")
result=read_pdf(file_path)
print("Total Pages:",result["page_count"])
print("\nExtracted text:")
print(result["text"])

print("\nPages without extractable text:")
print(result["empty_pages"])
