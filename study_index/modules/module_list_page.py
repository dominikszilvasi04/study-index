from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QLineEdit,
                               QListWidget, QListWidgetItem, QMessageBox,
                               QPushButton, QVBoxLayout, QWidget)
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import Module
from study_index.modules.module_details_form import ModuleDetailsForm


class ModuleListPage(QWidget):
    module_open_requested = Signal(object)
    title_label: QLabel
    description_label: QLabel
    search_input: QLineEdit
    empty_message: QLabel
    modules_list: QListWidget
    add_module_button: QPushButton
    open_module_button: QPushButton
    edit_module_button: QPushButton
    delete_module_button: QPushButton

    def __init__(self, module_database: ModuleDatabase) -> None:
        super().__init__()
        self.setObjectName("moduleListPage")
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.load_modules()

    def create_widgets(self) -> None:
        self.title_label = QLabel("Modules")
        self.title_label.setObjectName("pageTitle")
        self.description_label = QLabel("Organise your modules and open their linked study files.")
        self.description_label.setObjectName("pageDescription")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search modules")
        self.search_input.setClearButtonEnabled(True)
        self.empty_message = QLabel("No modules yet\nAdd your first module to get started.")
        self.empty_message.setObjectName("moduleEmptyMessage")
        self.modules_list = QListWidget()
        self.modules_list.setObjectName("modulesList")
        self.add_module_button = QPushButton("Add Module")
        self.add_module_button.setObjectName("primaryActionButton")
        self.open_module_button = QPushButton("Open Module")
        self.edit_module_button = QPushButton("Edit Module")
        self.delete_module_button = QPushButton("Delete Module")
        self.delete_module_button.setObjectName("dangerActionButton")
        self.open_module_button.setEnabled(False)
        self.edit_module_button.setEnabled(False)
        self.delete_module_button.setEnabled(False)

    def create_layout(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(30, 24, 30, 30)
        page_layout.setSpacing(18)
        page_layout.addLayout(self.create_header_layout())
        page_layout.addWidget(self.search_input)
        page_layout.addWidget(self.empty_message, 1)
        page_layout.addWidget(self.modules_list, 1)
        page_layout.addLayout(self.create_action_layout())

    def create_header_layout(self) -> QHBoxLayout:
        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(4)
        heading_layout.addWidget(self.title_label)
        heading_layout.addWidget(self.description_label)

        header_layout = QHBoxLayout()
        header_layout.addLayout(heading_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.add_module_button)
        return header_layout

    def create_action_layout(self) -> QHBoxLayout:
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)
        action_layout.addWidget(self.open_module_button)
        action_layout.addWidget(self.edit_module_button)
        action_layout.addWidget(self.delete_module_button)
        action_layout.addStretch()
        return action_layout

    def connect_signals(self) -> None:
        self.add_module_button.clicked.connect(self.add_module)
        self.open_module_button.clicked.connect(self.open_module_button_clicked)
        self.edit_module_button.clicked.connect(self.edit_module)
        self.delete_module_button.clicked.connect(self.delete_module)
        self.modules_list.currentItemChanged.connect(self.module_selection_changed)
        self.modules_list.itemActivated.connect(self.module_item_activated)
        self.search_input.textChanged.connect(self.filter_modules)

    def load_modules(self) -> None:
        for module in self.module_database.get_modules():
            self.add_module_item(module)
        self.update_empty_state()

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
        self.filter_modules(self.search_input.text())

    def edit_module(self) -> None:
        item = self.selected_module_item()
        self.filter_modules(self.search_input.text())
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
        self.filter_modules(self.search_input.text())

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

    def filter_modules(self, search_text: str) -> None:
        normalised_search = search_text.strip().casefold()
        for row_number in range(self.modules_list.count()):
            item = self.modules_list.item(row_number)
            module = item.data(Qt.ItemDataRole.UserRole)
            searchable_text = " ".join((module.name, module.code, module.term)).casefold()
            item.setHidden(normalised_search not in searchable_text)
        self.update_empty_state()


    # ------------------------------ Utilities ------------------------------

    def add_module_item(self, module: Module) -> None:
        item = QListWidgetItem()
        self.update_module_item(item, module)
        self.modules_list.addItem(item)

    @staticmethod
    def update_module_item(item: QListWidgetItem, module: Module) -> None:
        description = module.name
        module_details = " · ".join(value for value in (module.code, module.term) if value)
        if module_details:
            description += f"\n{module_details}"
        item.setText(description)
        item.setData(Qt.ItemDataRole.UserRole, module)

    def update_empty_state(self) -> None:
        if self.modules_list.count() == 0:
            self.show_empty_message("No modules yet\nAdd your first module to get started.")
            return
        if self.has_visible_modules():
            self.show_module_list()
            return
        self.show_empty_message("No modules match your search.")

    def has_visible_modules(self) -> bool:
        for row_number in range(self.modules_list.count()):
            if not self.modules_list.item(row_number).isHidden():
                return True
        return False

    def show_module_list(self) -> None:
        self.modules_list.show()
        self.empty_message.hide()

    def show_empty_message(self, message: str) -> None:
        self.empty_message.setText(message)
        self.modules_list.hide()
        self.empty_message.show()

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
