from PySide6.QtWidgets import (QInputDialog, QLabel, QListWidget, QMessageBox,
                               QPushButton, QVBoxLayout, QWidget)


class ModulesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.empty_message = QLabel("No Modules Available")
        self.modules_list = QListWidget()
        self.add_module_button = QPushButton("Add Module")
        self.page_layout = QVBoxLayout()
        self.page_layout.addWidget(self.empty_message)
        self.page_layout.addWidget(self.modules_list)
        self.page_layout.addWidget(self.add_module_button)
        self.setLayout(self.page_layout)
        self.add_module_button.clicked.connect(self.add_module)

    def add_module(self) -> None:
        module_name, accepted = QInputDialog.getText(self, "Add Module", "Module name:")
        if not accepted:
            return
        module_name = module_name.strip()
        if not module_name:
            QMessageBox.warning(self, "Warning", "Module name cannot be empty")
            return
        self.modules_list.addItem(module_name)
        self.empty_message.hide()