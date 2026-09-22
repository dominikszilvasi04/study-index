from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QAbstractItemView, QHeaderView, QTreeWidget,
                               QTreeWidgetItem)
from study_index.formatters import format_file_size, format_timestamp
from study_index.modules.models import FileMetadata


class ModuleFilesTable(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabels(["Name", "Type", "Size", "Modified", "Folder"])
        self.setRootIsDecorated(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def add_file(self, folder_path: str, file_metadata: FileMetadata) -> None:
        file_item = self.create_file_item(folder_path, file_metadata)
        self.addTopLevelItem(file_item)

    def create_file_item(self, folder_path: str,
                         file_metadata: FileMetadata) -> QTreeWidgetItem:
        file_item = QTreeWidgetItem([file_metadata.file_name,
                                     file_metadata.extension,
                                     format_file_size(file_metadata.size_bytes),
                                     format_timestamp(file_metadata.modified_timestamp),
                                     folder_path])
        file_item.setData(0, Qt.ItemDataRole.UserRole, file_metadata.full_path)
        return file_item
