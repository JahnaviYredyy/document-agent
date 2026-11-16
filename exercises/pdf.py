from pathlib import Path
from pypdf import PdfReader, PdfWriter

source=Path("samples/sample.pdf")
reader=PdfReader(source)
writer=PdfWriter()

writer.add_blank_page(width=62, height=792)
output=Path("samples/no_text.pdf")

with output.open("wb")as file:
    writer.write(file)
print("No-text pdf created:",output)
