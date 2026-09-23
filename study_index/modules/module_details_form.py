from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QLineEdit,
                               QMessageBox, QWidget)
from study_index.modules.models import Module


class ModuleDetailsForm(QDialog):
    def __init__(self, parent: QWidget, title: str, module: Module | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.name_input = QLineEdit()
        self.code_input = QLineEdit()
        self.term_input = QLineEdit()
        self.code_input.setPlaceholderText("Optional, e.g. CS444")
        self.term_input.setPlaceholderText("Optional, e.g. 2026/27 Semester 1")
        if module is not None:
            self.name_input.setText(module.name)
            self.code_input.setText(module.code)
            self.term_input.setText(module.term)
        layout = QFormLayout(self)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Code:", self.code_input)
        layout.addRow("Term:", self.term_input)
        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Module name cannot be empty")
            return
        super().accept()
