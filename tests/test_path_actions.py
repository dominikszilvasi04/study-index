import pytest
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

from study_index.path_actions import copy_path, open_path


def test_open_and_copy_paths(qapp: QApplication,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    parent = QWidget()
    warnings: list[str] = []
    opened_paths: list[str] = []
    monkeypatch.setattr(QDesktopServices, "openUrl",
                        lambda url: opened_paths.append(url.toLocalFile()) or True)
    monkeypatch.setattr(QMessageBox, "warning",
                        lambda parent, title, message: warnings.append(message))
    open_path(parent, "C:/College/notes.pdf")
    assert opened_paths == ["C:/College/notes.pdf"]
    assert warnings == []
    monkeypatch.setattr(QDesktopServices, "openUrl", lambda url: False)
    open_path(parent, "C:/Missing")
    assert warnings == ["Could not open:\nC:/Missing"]
    copy_path("C:/College/notes.pdf")
    assert QApplication.clipboard().text() == "C:/College/notes.pdf"
