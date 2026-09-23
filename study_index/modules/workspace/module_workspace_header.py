from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from study_index.modules.models import Module


class ModuleWorkspaceHeader(QWidget):
    module_list_requested = Signal()
    refresh_requested = Signal()

    def __init__(self, module: Module) -> None:
        super().__init__()
        self.back_button = QPushButton("←  Back to Modules")
        self.back_button.setObjectName("workspaceBackButton")
        self.module_name_label = QLabel(module.name)
        self.module_name_label.setObjectName("moduleNameLabel")
        module_details = " · ".join(value for value in (module.code, module.term) if value)
        self.module_details_label = QLabel(module_details)
        self.module_details_label.setObjectName("moduleDetailsLabel")
        self.refresh_button = QPushButton("Refresh")
        self.create_layout()
        self.module_details_label.setVisible(bool(module_details))
        self.connect_signals()

    def create_layout(self) -> None:
        header_layout = QVBoxLayout(self)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(18)
        header_layout.addWidget(self.back_button)
        header_layout.addLayout(self.create_module_heading_layout())

    def create_module_heading_layout(self) -> QHBoxLayout:
        module_details_layout = QVBoxLayout()
        module_details_layout.setSpacing(4)
        module_details_layout.addWidget(self.module_name_label)
        module_details_layout.addWidget(self.module_details_label)

        heading_layout = QHBoxLayout()
        heading_layout.addLayout(module_details_layout)
        heading_layout.addStretch()
        heading_layout.addWidget(self.refresh_button)
        return heading_layout

    def connect_signals(self) -> None:
        self.back_button.clicked.connect(self.module_list_requested.emit)
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
