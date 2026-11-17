from pathlib import Path
from pypdf import PdfReader

def read_pdf(file_path:Path)->dict:
    """Extract text from each page of a pdf"""

    reader=PdfReader(file_path)  #Loads PDF
    pages=[]
    empty_pages=[]

    for page_number, page in enumerate(reader.pages,start=1):
        text=page.extract_text() or ""
        pages.append({
            "page_number":page_number,
            "text":text
        })

        if not text.strip():
            empty_pages.append(page_number)

    full_text="\n".join(
        page["text"]for page in pages
    )

    return{
        "page_count":len(reader.pages),
        "pages":pages,
        "text": full_text,
        "empty_pages": empty_pages
    }