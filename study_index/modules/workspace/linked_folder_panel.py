from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import (QFileDialog, QFrame, QHBoxLayout, QLabel,
                               QListWidget, QListWidgetItem, QMenu, QMessageBox,
                               QPushButton, QVBoxLayout)
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import LinkedFolder, Module
from study_index.path_actions import copy_path, open_path


class LinkedFolderPanel(QFrame):
    folders_changed = Signal()
    title_label: QLabel
    folder_count_label: QLabel
    empty_message: QLabel
    linked_folders_list: QListWidget
    add_folder_button: QPushButton
    remove_folder_button: QPushButton
    locate_folder_button: QPushButton

    def __init__(self, module: Module,
                 module_database: ModuleDatabase) -> None:
        super().__init__()
        self.setObjectName("linkedFolderPanel")
        self.module = module
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.load_linked_folders()

    def create_widgets(self) -> None:
        self.title_label = QLabel("Linked Folders")
        self.title_label.setObjectName("workspacePanelTitle")
        self.folder_count_label = QLabel()
        self.folder_count_label.setObjectName("workspaceCountLabel")
        self.empty_message = self.create_empty_message()
        self.linked_folders_list = self.create_folders_list()
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.setObjectName("primaryActionButton")
        self.remove_folder_button = QPushButton("Remove Folder")
        self.remove_folder_button.setObjectName("dangerActionButton")
        self.remove_folder_button.setEnabled(False)
        self.locate_folder_button = QPushButton("Locate Folder")
        self.locate_folder_button.setEnabled(False)

    @staticmethod
    def create_empty_message() -> QLabel:
        empty_message = QLabel("No Folders Linked")
        empty_message.setObjectName("folderEmptyMessage")
        empty_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return empty_message

    @staticmethod
    def create_folders_list() -> QListWidget:
        folders_list = QListWidget()
        folders_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        folders_list.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        folders_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        return folders_list

    def create_layout(self) -> None:
        panel_layout = QVBoxLayout(self)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)

        panel_layout.addLayout(self.create_header_layout())
        panel_layout.addWidget(self.empty_message, 1)
        panel_layout.addWidget(self.linked_folders_list, 1)
        panel_layout.addWidget(self.create_action_bar())

    def create_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(8)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.folder_count_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_folder_button)
        return header_layout

    def create_action_bar(self) -> QFrame:
        action_bar = QFrame()
        action_bar.setObjectName("folderActionBar")
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(14, 10, 14, 10)
        action_layout.setSpacing(6)
        action_layout.addWidget(self.locate_folder_button)
        action_layout.addWidget(self.remove_folder_button)
        action_layout.addStretch()
        return action_bar

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
        folder_count = self.linked_folders_list.count()
        self.folder_count_label.setText(f"({folder_count})")
        self.empty_message.setVisible(folder_count == 0)
        self.linked_folders_list.setVisible(folder_count > 0)

    def folder_selection_changed(self, current_item: QListWidgetItem | None) -> None:
        self.remove_folder_button.setEnabled(current_item is not None)
        self.locate_folder_button.setEnabled(current_item is not None)

    def selected_folder_item(self) -> QListWidgetItem:
        folder_item = self.linked_folders_list.currentItem()
        if folder_item is None:
            raise RuntimeError("A linked folder must be selected")
        return folder_item
