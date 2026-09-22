from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QLabel, QListWidget, QListWidgetItem,
                               QMenu, QMessageBox, QPushButton, QVBoxLayout, QWidget)
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import LinkedFolder, Module
from study_index.path_actions import copy_path, open_path


class LinkedFolderPanel(QWidget):
    folders_changed = Signal()

    def __init__(self, module: Module,
                 module_database: ModuleDatabase) -> None:
        super().__init__()
        self.module = module
        self.module_database = module_database
        self.title_label = QLabel("Linked Folders")
        self.empty_message = QLabel("No Folders Linked")
        self.linked_folders_list = QListWidget()
        self.linked_folders_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.add_folder_button = QPushButton("Add Folder")
        self.remove_folder_button = QPushButton("Remove Folder")
        self.remove_folder_button.setEnabled(False)
        self.locate_folder_button = QPushButton("Locate Folder")
        self.locate_folder_button.setEnabled(False)
        self.create_layout()
        self.connect_signals()
        self.load_linked_folders()

    def create_layout(self) -> None:
        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.title_label)
        panel_layout.addWidget(self.empty_message)
        panel_layout.addWidget(self.linked_folders_list)
        panel_layout.addWidget(self.add_folder_button)
        panel_layout.addWidget(self.remove_folder_button)
        panel_layout.addWidget(self.locate_folder_button)
        self.setLayout(panel_layout)

    def connect_signals(self) -> None:
        self.add_folder_button.clicked.connect(self.add_folder)
        self.remove_folder_button.clicked.connect(self.remove_folder)
        self.linked_folders_list.currentItemChanged.connect(self.folder_selection_changed)
        self.locate_folder_button.clicked.connect(self.locate_folder)
        self.linked_folders_list.itemActivated.connect(self.open_folder)
        self.linked_folders_list.customContextMenuRequested.connect(self.show_context_menu)

    def open_folder(self, item: QListWidgetItem) -> None:
        open_path(self, item.text())

    @staticmethod
    def copy_folder_path(item: QListWidgetItem) -> None:
        copy_path(item.text())

    def show_context_menu(self, position: QPoint) -> None:
        item = self.linked_folders_list.itemAt(position)
        if item is None:
            return
        self.linked_folders_list.setCurrentItem(item)
        menu = QMenu(self)
        open_action = menu.addAction("Open Folder")
        copy_action = menu.addAction("Copy Path")
        selected_action = menu.exec(self.linked_folders_list.viewport().mapToGlobal(position))
        if selected_action == open_action:
            self.open_folder(item)
        elif selected_action == copy_action:
            self.copy_folder_path(item)

    def load_linked_folders(self) -> None:
        for linked_folder in self.module_database.get_linked_folders(self.module.id):
            self.add_linked_folder_item(linked_folder)

        self.update_empty_message()

    def add_linked_folder_item(self, linked_folder: LinkedFolder) -> None:
        folder_item = QListWidgetItem(linked_folder.path)
        folder_item.setData(Qt.ItemDataRole.UserRole, linked_folder.id)
        self.linked_folders_list.addItem(folder_item)

    def add_folder(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, "Add Folder")
        if not folder_path:
            return

        linked_folder = self.module_database.add_linked_folder(self.module.id, folder_path)
        if linked_folder is None:
            QMessageBox.warning(self, "Warning", "Folder is already linked")
            return

        self.add_linked_folder_item(linked_folder)
        self.update_empty_message()
        self.folders_changed.emit()

    def locate_folder(self) -> None:
        folder_item = self.selected_folder_item()
        folder_path = QFileDialog.getExistingDirectory(self, "Locate Folder")
        if not folder_path:
            return
        linked_folder_id = folder_item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.relocate_linked_folder(linked_folder_id, folder_path):
            QMessageBox.warning(self, "Locate Folder", "Folder is already linked, or link may no longer exist")
            return
        folder_item.setText(folder_path)
        self.folders_changed.emit()

    def remove_folder(self) -> None:
        folder_item = self.selected_folder_item()
        answer = QMessageBox.question(self, "Remove Folder", f'Remove "{folder_item.text()}"?')
        if answer != QMessageBox.StandardButton.Yes:
            return

        linked_folder_id = folder_item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.remove_linked_folder(linked_folder_id):
            return

        self.linked_folders_list.takeItem(self.linked_folders_list.row(folder_item))
        self.update_empty_message()
        self.folders_changed.emit()

    def update_empty_message(self) -> None:
        self.empty_message.setVisible(self.linked_folders_list.count() == 0)

    def folder_selection_changed(self, current_item: QListWidgetItem | None) -> None:
        self.remove_folder_button.setEnabled(current_item is not None)
        self.locate_folder_button.setEnabled(current_item is not None)

    def selected_folder_item(self) -> QListWidgetItem:
        folder_item = self.linked_folders_list.currentItem()
        if folder_item is None:
            raise RuntimeError("A linked folder must be selected")
        return folder_item
