from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)

from study_index.modules.models import LinkedFolder, Module


class LinkedFolderPanel(QWidget):
    folders_changed = Signal()

    def __init__(self, module: Module, module_database):
        super().__init__()
        self.module = module
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.load_linked_folders()

    def create_widgets(self) -> None:
        self.title_label = QLabel("Linked Folders")
        self.empty_message = QLabel("No Folders Linked")
        self.linked_folders_list = QListWidget()
        self.add_folder_button = QPushButton("Add Folder")
        self.remove_folder_button = QPushButton("Remove Folder")
        self.remove_folder_button.setEnabled(False)

    def create_layout(self) -> None:
        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.title_label)
        panel_layout.addWidget(self.empty_message)
        panel_layout.addWidget(self.linked_folders_list)
        panel_layout.addWidget(self.add_folder_button)
        panel_layout.addWidget(self.remove_folder_button)
        self.setLayout(panel_layout)

    def connect_signals(self) -> None:
        self.add_folder_button.clicked.connect(self.add_folder)
        self.remove_folder_button.clicked.connect(self.remove_folder)
        self.linked_folders_list.currentItemChanged.connect(self.folder_selection_changed)

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

    def remove_folder(self) -> None:
        folder_item = self.linked_folders_list.currentItem()
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

    def folder_selection_changed(self, current_item) -> None:
        self.remove_folder_button.setEnabled(current_item is not None)
