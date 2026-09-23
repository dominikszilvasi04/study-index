from pathlib import Path

import pytest
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

from study_index.path_actions import copy_path, open_path


def test_open_and_copy_paths(tmp_path: Path, qapp: QApplication,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    parent = QWidget()
    file_path = tmp_path / "notes.pdf"
    missing_path = tmp_path / "Missing"
    warnings: list[str] = []
    opened_paths: list[str] = []
    monkeypatch.setattr(QDesktopServices, "openUrl",
                        lambda url: opened_paths.append(url.toLocalFile()) or True)
    monkeypatch.setattr(QMessageBox, "warning",
                        lambda parent, title, message: warnings.append(message))
    open_path(parent, str(file_path))
    assert [Path(path) for path in opened_paths] == [file_path]
    assert warnings == []
    monkeypatch.setattr(QDesktopServices, "openUrl", lambda url: False)
    open_path(parent, str(missing_path))
    assert warnings == [f"Could not open:\n{missing_path}"]
    copy_path(str(file_path))
    assert QApplication.clipboard().text() == str(file_path)
