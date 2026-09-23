from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QLabel,
                               QLineEdit, QVBoxLayout, QWidget, QMessageBox)
from study_index.modules.models import Module


class ModuleDetailsForm(QDialog):
    title_label: QLabel
    description_label: QLabel
    name_input: QLineEdit
    code_input: QLineEdit
    term_input: QLineEdit
    button_box: QDialogButtonBox

    def __init__(self, parent: QWidget, title: str,
                 module: Module | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("moduleDetailsForm")
        self.setMinimumWidth(440)
        self.setWindowTitle(title)
        self.create_widgets(title, module)
        self.create_layout()
        self.connect_signals()

    def create_widgets(self, title: str,
                       module: Module | None) -> None:
        self.title_label = QLabel(title)
        self.title_label.setObjectName("dialogTitle")
        if module is None:
            description = "Create a module for organising related study files."
        else:
            description = "Update this module's name and academic details."
        self.description_label = QLabel(description)
        self.description_label.setObjectName("dialogDescription")
        self.description_label.setWordWrap(True)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Machine Learning")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g. CS401")
        self.term_input = QLineEdit()
        self.term_input.setPlaceholderText("e.g. Semester 1")
        self.button_box = self.create_button_box()
        self.populate_fields(module)

    def create_layout(self) -> None:
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(16)
        form_layout.setVerticalSpacing(12)
        form_layout.addRow("Name", self.name_input)
        form_layout.addRow("Code (optional)", self.code_input)
        form_layout.addRow("Term (optional)", self.term_input)
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(24, 22, 24, 20)
        dialog_layout.setSpacing(16)
        dialog_layout.addWidget(self.title_label)
        dialog_layout.addWidget(self.description_label)
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(self.button_box)

    def connect_signals(self) -> None:
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Module name cannot be empty")
            return
        super().accept()

    # ------------------------------ Utilities ------------------------------

    @staticmethod
    def create_button_box() -> QDialogButtonBox:
        button_box = QDialogButtonBox()
        save_button = button_box.addButton(
            QDialogButtonBox.StandardButton.Save)
        save_button.setObjectName("primaryActionButton")
        button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        return button_box

    def populate_fields(self, module: Module | None) -> None:
        if module is None:
            return
        self.name_input.setText(module.name)
        self.code_input.setText(module.code)
        self.term_input.setText(module.term)