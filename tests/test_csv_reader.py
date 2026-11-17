
import pytest

from document_agent.csv_reader import read_csv


def test_read_valid_csv(tmp_path):
    # Create a CSV file
    csv_file = tmp_path / "employees.csv"

    csv_file.write_text(
        "id,name\n001,Asha\n002,Ravi",
        encoding="utf-8"
    )

    # Read the CSV
    result = read_csv(csv_file)

    # Check the contents
    assert len(result) == 2
    assert result[0]["name"] == "Asha"
    assert result[1]["name"] == "Ravi"


def test_csv_preserves_leading_zeros(tmp_path):
    csv_file = tmp_path / "employees.csv"

    csv_file.write_text(
        "id,name\n001,Asha",
        encoding="utf-8"
    )

    result = read_csv(csv_file)

    # ID should remain a string
    assert result[0]["id"] == "001"


def test_empty_csv_raises_error(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        read_csv(csv_file)


def test_duplicate_headers_raise_error(tmp_path):
    csv_file = tmp_path / "duplicate.csv"

    csv_file.write_text(
        "id,name,name\n001,Asha,Ravi",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        read_csv(csv_file)


def test_wrong_number_of_columns_raises_error(tmp_path):
    csv_file = tmp_path / "invalid.csv"

    csv_file.write_text(
        "id,name\n001,Asha,Extra",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        read_csv(csv_file)
