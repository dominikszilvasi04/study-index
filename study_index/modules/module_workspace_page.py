from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)
from study_index.modules.models import LinkedFolder, Module


class ModuleWorkspacePage(QWidget):
    module_list_requested = Signal()

    def __init__(self, module: Module, module_database):
        super().__init__()
        self.module = module
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.load_linked_folders()

    def create_widgets(self) -> None:
        self.module_name_label = QLabel(self.module.name)
        self.empty_message = QLabel("No Folders Linked")
        self.linked_folders_list = QListWidget()
        self.add_folder_button = QPushButton("Add Folder")
        self.remove_folder_button = QPushButton("Remove Folder")
        self.back_button = QPushButton("Back to Modules")
        self.remove_folder_button.setEnabled(False)

    def create_layout(self) -> None:
        page_layout = QVBoxLayout()
        page_layout.addWidget(self.module_name_label)
        page_layout.addWidget(self.empty_message)
        page_layout.addWidget(self.linked_folders_list)
        page_layout.addWidget(self.add_folder_button)
        page_layout.addWidget(self.remove_folder_button)
        page_layout.addWidget(self.back_button)
        self.setLayout(page_layout)

    def connect_signals(self) -> None:
        self.add_folder_button.clicked.connect(self.add_folder)
        self.remove_folder_button.clicked.connect(self.remove_folder)
        self.back_button.clicked.connect(self.module_list_requested.emit)
        self.linked_folders_list.currentItemChanged.connect(self.folder_selection_changed)

    def load_linked_folders(self) -> None:
        for linked_folder in self.module_database.get_linked_folders(self.module.id):
            self.add_linked_folder_item(linked_folder)
        self.empty_message.setVisible(self.linked_folders_list.count() == 0)

    def add_linked_folder_item(self, linked_folder: LinkedFolder) -> None:
        item = QListWidgetItem(linked_folder.path)
        item.setData(Qt.ItemDataRole.UserRole, linked_folder.id)
        self.linked_folders_list.addItem(item)

    def add_folder(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, "Add Folder")
        if not folder_path:
            return
        linked_folder = self.module_database.add_linked_folder(self.module.id, folder_path)
        if linked_folder is None:
            QMessageBox.warning(self, "Warning", "Folder is already linked")
            return
        self.add_linked_folder_item(linked_folder)
        self.empty_message.hide()

    def remove_folder(self) -> None:
        item = self.linked_folders_list.currentItem()
        answer = QMessageBox.question(self, "Remove Folder", f'Remove "{item.text()}"?')
        if answer != QMessageBox.StandardButton.Yes:
            return
        linked_folder_id = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.remove_linked_folder(linked_folder_id):
            return
        self.linked_folders_list.takeItem(self.linked_folders_list.row(item))
        self.empty_message.setVisible(self.linked_folders_list.count() == 0)

    def folder_selection_changed(self, current_item) -> None:
        self.remove_folder_button.setEnabled(current_item is not None)
