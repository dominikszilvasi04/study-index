from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QInputDialog, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import Module


class ModuleListPage(QWidget):
    module_open_requested = Signal(object)

    def __init__(self, module_database: ModuleDatabase) -> None:
        super().__init__()
        self.module_database = module_database
        self.empty_message = QLabel("No Modules Available")
        self.modules_list = QListWidget()
        self.add_module_button = QPushButton("Add Module")
        self.open_module_button = QPushButton("Open Module")
        self.edit_module_button = QPushButton("Edit Module")
        self.delete_module_button = QPushButton("Delete Module")
        self.open_module_button.setEnabled(False)
        self.edit_module_button.setEnabled(False)
        self.delete_module_button.setEnabled(False)
        self.create_layout()
        self.connect_signals()
        self.load_modules()

    def create_layout(self) -> None:
        page_layout = QVBoxLayout()
        page_layout.addWidget(self.empty_message)
        page_layout.addWidget(self.modules_list)
        page_layout.addWidget(self.add_module_button)
        page_layout.addWidget(self.open_module_button)
        page_layout.addWidget(self.edit_module_button)
        page_layout.addWidget(self.delete_module_button)
        self.setLayout(page_layout)

    def connect_signals(self) -> None:
        self.add_module_button.clicked.connect(self.add_module)
        self.open_module_button.clicked.connect(self.request_module_open)
        self.edit_module_button.clicked.connect(self.edit_module)
        self.delete_module_button.clicked.connect(self.delete_module)
        self.modules_list.currentItemChanged.connect(self.module_selection_changed)

    def load_modules(self) -> None:
        for module in self.module_database.get_modules():
            self.add_module_item(module)
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def add_module_item(self, module: Module) -> None:
        item = QListWidgetItem(module.name)
        item.setData(Qt.ItemDataRole.UserRole, module.id)
        self.modules_list.addItem(item)

    def add_module(self) -> None:
        module_name = self.request_module_name("Add Module")
        if module_name is None:
            return
        module = self.module_database.add_module(module_name)
        if module is None:
            QMessageBox.warning(self, "Warning", "Module name already exists")
            return
        self.add_module_item(module)
        self.empty_message.hide()

    def edit_module(self) -> None:
        item = self.selected_module_item()
        module_name = self.request_module_name("Edit Module", item.text())
        if module_name is None:
            return
        module_id = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.rename_module(module_id, module_name):
            QMessageBox.warning(self, "Warning", "Module name already exists")
            return
        item.setText(module_name)

    def delete_module(self) -> None:
        item = self.selected_module_item()
        answer = QMessageBox.question(self, "Delete Module", f'Delete "{item.text()}"?')
        if answer != QMessageBox.StandardButton.Yes:
            return
        module_id = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.delete_module(module_id):
            return
        self.modules_list.takeItem(self.modules_list.row(item))
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def module_selection_changed(self,
                                 current_item: QListWidgetItem | None) -> None:
        module_selected = current_item is not None
        self.open_module_button.setEnabled(module_selected)
        self.edit_module_button.setEnabled(module_selected)
        self.delete_module_button.setEnabled(module_selected)

    def request_module_open(self) -> None:
        item = self.selected_module_item()
        module_id = item.data(Qt.ItemDataRole.UserRole)
        self.module_open_requested.emit(Module(module_id, item.text()))

    def selected_module_item(self) -> QListWidgetItem:
        item = self.modules_list.currentItem()
        if item is None:
            raise RuntimeError("A module must be selected")
        return item

    def request_module_name(self, title: str,
                            current_name: str = "") -> str | None:
        module_name, accepted = QInputDialog.getText(self, title, "Module name:", text=current_name)
        if not accepted:
            return None
        module_name = module_name.strip()
        if not module_name:
            QMessageBox.warning(self, "Warning", "Module name cannot be empty")
            return None
        return module_name
