from datetime import datetime

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from study_index.modules.models import FileMetadata
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
