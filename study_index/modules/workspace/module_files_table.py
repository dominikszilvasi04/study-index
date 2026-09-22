from pathlib import Path
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (QAbstractItemView, QHeaderView, QMenu,
                               QTreeWidget, QTreeWidgetItem)
from study_index.formatters import format_file_size, format_timestamp
from study_index.modules.models import FileMetadata
from study_index.path_actions import copy_path, open_path


class ModuleFilesTable(QTreeWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setHeaderLabels(["Name", "Type", "Size", "Modified", "Folder"])
        self.setRootIsDecorated(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.connect_signals()

    def connect_signals(self) -> None:
        self.itemActivated.connect(self.open_file)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def add_file(self, folder_path: str, file_metadata: FileMetadata) -> None:
        file_item = self.create_file_item(folder_path, file_metadata)
        self.addTopLevelItem(file_item)

    def open_file(self, item: QTreeWidgetItem, column: int) -> None:
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        open_path(self, file_path)

    def show_context_menu(self, position: QPoint) -> None:
        item = self.itemAt(position)
        if item is None:
            return
        self.setCurrentItem(item)
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        folder_action = menu.addAction("Open Containing Folder")
        copy_action = menu.addAction("Copy Path")
        selected_action = menu.exec(self.viewport().mapToGlobal(position))
        if selected_action == open_action:
            self.open_file(item, 0)
        elif selected_action == folder_action:
            self.open_containing_folder(item)
        elif selected_action == copy_action:
            self.copy_file_path(item)

    def open_containing_folder(self, item: QTreeWidgetItem) -> None:
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        folder_path = str(Path(file_path).parent)
        open_path(self, folder_path)

    @staticmethod
    def copy_file_path(item: QTreeWidgetItem) -> None:
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        copy_path(file_path)

    @staticmethod
    def create_file_item(folder_path: str, file_metadata: FileMetadata) -> QTreeWidgetItem:
        file_item = QTreeWidgetItem([file_metadata.file_name,
                                     file_metadata.extension,
                                     format_file_size(file_metadata.size_bytes),
                                     format_timestamp(file_metadata.modified_timestamp),
                                     folder_path])
        file_item.setData(0, Qt.ItemDataRole.UserRole, file_metadata.full_path)
        return file_item
