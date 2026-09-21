from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QInputDialog, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)

from study_index.modules.modules_model import Module


class ModulesPage(QWidget):
    def __init__(self, module_repository):
        super().__init__()
        self.module_repository = module_repository
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.load_modules()

    def create_widgets(self) -> None:
        self.empty_message = QLabel("No Modules Available")
        self.modules_list = QListWidget()
        self.add_module_button = QPushButton("Add Module")
        self.edit_module_button = QPushButton("Edit Module")
        self.delete_module_button = QPushButton("Delete Module")
        self.edit_module_button.setEnabled(False)
        self.delete_module_button.setEnabled(False)

    def create_layout(self) -> None:
        page_layout = QVBoxLayout()
        page_layout.addWidget(self.empty_message)
        page_layout.addWidget(self.modules_list)
        page_layout.addWidget(self.add_module_button)
        page_layout.addWidget(self.edit_module_button)
        page_layout.addWidget(self.delete_module_button)
        self.setLayout(page_layout)

    def connect_signals(self) -> None:
        self.add_module_button.clicked.connect(self.add_module)
        self.edit_module_button.clicked.connect(self.edit_module)
        self.delete_module_button.clicked.connect(self.delete_module)
        self.modules_list.currentItemChanged.connect(self.module_selection_changed)

    def load_modules(self) -> None:
        for module in self.module_repository.all():
            self.add_module_item(module)
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def add_module_item(self, module: Module) -> None:
        item = QListWidgetItem(module.name)
        item.setData(Qt.ItemDataRole.UserRole, module.id)
        self.modules_list.addItem(item)

    def add_module(self) -> None:
        module_name, accepted = QInputDialog.getText(self, "Add Module", "Module name:")
        if not accepted:
            return
        module_name = module_name.strip()
        if not module_name:
            QMessageBox.warning(self,"Warning","Module name cannot be empty")
            return
        module = self.module_repository.add(module_name)
        if module is None:
            QMessageBox.warning(self,"Warning","Module name already exists")
            return
        self.add_module_item(module)
        self.empty_message.hide()

    def edit_module(self) -> None:
        item = self.modules_list.currentItem()
        module_name, accepted = QInputDialog.getText(self, "Edit Module", "Module name:", text=item.text())
        if not accepted:
            return
        module_name = module_name.strip()
        if not module_name:
            QMessageBox.warning(self,"Warning","Module name cannot be empty")
            return
        module_id = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_repository.update(module_id, module_name):
            QMessageBox.warning(self,"Warning","Module name already exists")
            return
        item.setText(module_name)

    def delete_module(self) -> None:
        item = self.modules_list.currentItem()
        answer = QMessageBox.question(self, "Delete Module", f'Delete "{item.text()}"?')
        if answer != QMessageBox.StandardButton.Yes:
            return
        module_id = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_repository.delete(module_id):
            return
        self.modules_list.takeItem(self.modules_list.row(item))
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def module_selection_changed(self, current_item) -> None:
        module_selected = current_item is not None
        self.edit_module_button.setEnabled(module_selected)
        self.delete_module_button.setEnabled(module_selected)
