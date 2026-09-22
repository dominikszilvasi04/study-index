from pathlib import Path
import pytest
from PySide6.QtCore import QStandardPaths
from study_index.config import application_data_directory, database_path


def test_application_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_directory = Path("C:/StudyIndexData")
    monkeypatch.setattr(QStandardPaths, "writableLocation", lambda location: str(expected_directory))
    assert application_data_directory() == expected_directory
    assert database_path() == expected_directory / "study_index.db"
