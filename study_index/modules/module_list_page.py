from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QDialog, QLabel, QListWidget, QListWidgetItem,
                               QMessageBox, QPushButton, QVBoxLayout, QWidget)
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import Module
from study_index.modules.module_details_form import ModuleDetailsForm


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
        self.open_module_button.clicked.connect(self.open_module_button_clicked)
        self.edit_module_button.clicked.connect(self.edit_module)
        self.delete_module_button.clicked.connect(self.delete_module)
        self.modules_list.currentItemChanged.connect(self.module_selection_changed)
        self.modules_list.itemActivated.connect(self.module_item_activated)

    def load_modules(self) -> None:
        for module in self.module_database.get_modules():
            self.add_module_item(module)
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def add_module_item(self, module: Module) -> None:
        item = QListWidgetItem()
        self.update_module_item(item, module)
        self.modules_list.addItem(item)

    @staticmethod
    def update_module_item(item: QListWidgetItem, module: Module) -> None:
        description = module.name
        if module.code:
            description += f" ({module.code})"
        if module.term:
            description += f" — {module.term}"
        item.setText(description)
        item.setData(Qt.ItemDataRole.UserRole, module)

    def add_module(self) -> None:
        details = self.request_module_details("Add Module")
        if details is None:
            return
        name, code, term = details
        module = self.module_database.add_module(name, code, term)
        if module is None:
            QMessageBox.warning(self, "Warning", "Module name already exists")
            return
        self.add_module_item(module)
        self.empty_message.hide()

    def edit_module(self) -> None:
        item = self.selected_module_item()
        module = item.data(Qt.ItemDataRole.UserRole)
        details = self.request_module_details("Edit Module", module)
        if details is None:
            return
        name, code, term = details
        if not self.module_database.update_module(module.id, name, code, term):
            QMessageBox.warning(self, "Warning", "Module name already exists")
            return
        self.update_module_item(item, Module(module.id, name, code, term))

    def delete_module(self) -> None:
        item = self.selected_module_item()
        answer = QMessageBox.question(self, "Delete Module", f'Delete "{item.text()}"?')
        if answer != QMessageBox.StandardButton.Yes:
            return
        module = item.data(Qt.ItemDataRole.UserRole)
        if not self.module_database.delete_module(module.id):
            return
        self.modules_list.takeItem(self.modules_list.row(item))
        self.empty_message.setVisible(self.modules_list.count() == 0)

    def module_selection_changed(self,
                                 current_item: QListWidgetItem | None) -> None:
        module_selected = current_item is not None
        self.open_module_button.setEnabled(module_selected)
        self.edit_module_button.setEnabled(module_selected)
        self.delete_module_button.setEnabled(module_selected)

    def open_module_button_clicked(self) -> None:
        item = self.selected_module_item()
        module = item.data(Qt.ItemDataRole.UserRole)
        self.module_open_requested.emit(module)

    def module_item_activated(self, item: QListWidgetItem) -> None:
        module = item.data(Qt.ItemDataRole.UserRole)
        self.module_open_requested.emit(module)

    def selected_module_item(self) -> QListWidgetItem:
        item = self.modules_list.currentItem()
        if item is None:
            raise RuntimeError("A module must be selected")
        return item

    def request_module_details(self, title: str,
                               module: Module | None = None) -> tuple[str, str, str] | None:
        form = ModuleDetailsForm(self, title, module)
        if form.exec() != QDialog.DialogCode.Accepted:
            return None
        return (form.name_input.text().strip(),
                form.code_input.text().strip(),
                form.term_input.text().strip())
