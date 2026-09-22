from pathlib import Path
import pytest
from study_index.modules.workspace.file_finder import FileFinder


def test_find_files_returns_nested_files_in_path_order(tmp_path: Path) -> None:
    nested_directory = tmp_path / "Nested"
    nested_directory.mkdir()
    second_file = nested_directory / "second.PDF"
    first_file = tmp_path / "First.txt"
    second_file.write_text("PDF content")
    first_file.write_text("Text content")
    files = FileFinder(str(tmp_path)).find_files()
    assert [file.file_name for file in files] == ["First.txt", "second.PDF"]
    assert files[0].full_path == str(first_file)
    assert files[0].extension == ".txt"
    assert files[0].size_bytes == len("Text content")
    assert files[0].modified_timestamp == first_file.stat().st_mtime
    assert files[1].extension == ".pdf"


def test_find_files_returns_empty_list_for_empty_directory(tmp_path: Path) -> None:
    assert FileFinder(str(tmp_path)).find_files() == []


def test_find_files_rejects_missing_directory(tmp_path: Path) -> None:
    missing_directory = tmp_path / "Missing"
    with pytest.raises(NotADirectoryError, match="is not a directory"):
        FileFinder(str(missing_directory)).find_files()
