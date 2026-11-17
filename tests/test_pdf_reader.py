
import pytest
from pypdf import PdfWriter

from document_agent.pdf_reader import read_pdf


def create_blank_pdf(file_path):
    writer = PdfWriter()

    writer.add_blank_page(width=300, height=300)
    writer.add_blank_page(width=300, height=300)

    with open(file_path, "wb") as file:
        writer.write(file)


def test_read_pdf_page_count(tmp_path):
    pdf_file = tmp_path / "sample.pdf"

    create_blank_pdf(pdf_file)

    result = read_pdf(pdf_file)

    assert result["page_count"] == 2


def test_blank_pdf_pages_are_detected(tmp_path):
    pdf_file = tmp_path / "blank.pdf"

    create_blank_pdf(pdf_file)

    result = read_pdf(pdf_file)

    assert result["empty_pages"] == [1, 2]


def test_corrupt_pdf_raises_error(tmp_path):
    pdf_file = tmp_path / "corrupt.pdf"

    pdf_file.write_text(
        "This is not a valid PDF",
        encoding="utf-8"
    )

    with pytest.raises(Exception):
        read_pdf(pdf_file)
