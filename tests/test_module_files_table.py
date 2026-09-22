from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from study_index.modules.models import FileMetadata
from study_index.modules.workspace.module_files_table import ModuleFilesTable


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
