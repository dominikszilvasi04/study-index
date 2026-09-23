from datetime import datetime
from pathlib import Path

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication

from study_index.modules.models import FileMetadata
from study_index.modules.workspace import module_files_table
from study_index.modules.workspace.module_files_table import (FILE_MODIFIED_COLUMN,
                                                             FILE_NAME_COLUMN,
                                                             FILE_SIZE_COLUMN,
                                                             ModuleFilesTable)


def test_add_file_displays_metadata(qapp: QApplication) -> None:
    table = ModuleFilesTable()
    timestamp = datetime(2026, 9, 22, 14, 5).timestamp()
    metadata = FileMetadata("C:/College/notes.PDF",
                            "notes.PDF",
                            ".pdf",
                            1234,
                            timestamp)
    table.add_file("C:/College", metadata)
    item = table.topLevelItem(0)
    assert table.topLevelItemCount() == 1
    assert [item.text(column) for column in range(5)] == [
        "notes.PDF", ".pdf", "1,234", "2026-09-22 14:05", "C:/College"
    ]
    assert item.data(0, Qt.ItemDataRole.UserRole) == metadata.full_path


@pytest.mark.parametrize("column, expected_names", [
    (FILE_NAME_COLUMN, ["alpha.pdf", "Beta.pdf", "charlie.pdf"]),
    (FILE_SIZE_COLUMN, ["Beta.pdf", "charlie.pdf", "alpha.pdf"]),
    (FILE_MODIFIED_COLUMN, ["charlie.pdf", "alpha.pdf", "Beta.pdf"])
])
def test_sorting_uses_names_and_raw_numbers(qapp: QApplication,
                                           column: int, expected_names: list[str]) -> None:
    table = ModuleFilesTable()
    # Timestamps within one minute have identical displayed dates.
    for name, size, timestamp in [("Beta.pdf", 9, 1700000003),
                                   ("alpha.pdf", 1000, 1700000002),
                                   ("charlie.pdf", 80, 1700000001)]:
        table.add_file("C:/College", FileMetadata(f"C:/College/{name}", name,
                                                  ".pdf", size, timestamp))
    table.sortItems(column, Qt.SortOrder.AscendingOrder)
    assert [table.topLevelItem(row).text(FILE_NAME_COLUMN) for row in range(3)] == expected_names
    table.sortItems(column, Qt.SortOrder.DescendingOrder)
    assert [table.topLevelItem(row).text(FILE_NAME_COLUMN) for row in range(3)] == list(reversed(expected_names))


def test_filter_files(qapp: QApplication) -> None:
    table = ModuleFilesTable()
    table.add_file("C:/College", FileMetadata("C:/College/Notes.PDF", "Notes.PDF",
                                              ".pdf", 1, 1))
    table.add_file("C:/College", FileMetadata("C:/College/essay.docx", "essay.docx",
                                              ".docx", 1, 1))
    table.filter_files(" notes ", (".pdf",))
    rows = {table.topLevelItem(row_number).text(FILE_NAME_COLUMN): table.topLevelItem(row_number)
            for row_number in range(table.topLevelItemCount())}
    assert not rows["Notes.PDF"].isHidden()
    assert rows["essay.docx"].isHidden()
    table.filter_files("")
    assert not rows["Notes.PDF"].isHidden()
    assert not rows["essay.docx"].isHidden()


@pytest.mark.parametrize("selected_action", ["Open", "Open Containing Folder", "Copy Path"])
def test_file_actions_and_context_menu(qapp: QApplication,
                                       monkeypatch: pytest.MonkeyPatch,
                                       selected_action: str) -> None:
    table = ModuleFilesTable()
    table.add_file("C:/College", FileMetadata("C:/College/notes.pdf", "notes.pdf",
                                              ".pdf", 1, 1))
    item = table.topLevelItem(0)
    actions: list[tuple[str, str]] = []

    class FakeMenu:
        def __init__(self, parent: ModuleFilesTable) -> None:
            pass

        def addAction(self, text: str) -> str:
            return text

        def exec(self, position: QPoint) -> str:
            return selected_action

    monkeypatch.setattr(module_files_table, "QMenu", FakeMenu)
    monkeypatch.setattr(table, "itemAt", lambda position: item)
    monkeypatch.setattr(module_files_table, "open_path",
                        lambda parent, path: actions.append(("open", path)))
    monkeypatch.setattr(module_files_table, "copy_path",
                        lambda path: actions.append(("copy", path)))
    table.show_context_menu(QPoint())
    expected_path = str(Path("C:/College")) if selected_action == "Open Containing Folder" else "C:/College/notes.pdf"
    expected_action = "copy" if selected_action == "Copy Path" else "open"
    assert actions == [(expected_action, expected_path)]
    monkeypatch.setattr(table, "itemAt", lambda position: None)
    table.show_context_menu(QPoint())
