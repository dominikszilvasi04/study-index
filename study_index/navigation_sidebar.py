from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class NavigationSidebar(QFrame):
    modules_requested = Signal()
    events_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("navigationSidebar")
        self.setMinimumWidth(200)
        self.brand_label = QLabel("StudyIndex")
        self.brand_label.setObjectName("brandLabel")
        self.modules_button = QPushButton("Modules")
        self.modules_button.setObjectName("navigationButton")
        self.modules_button.setCheckable(True)
        self.modules_button.setChecked(True)
        self.modules_button.setAutoExclusive(True)
        self.events_button = QPushButton("Events")
        self.events_button.setObjectName("navigationButton")
        self.events_button.setCheckable(True)
        self.events_button.setAutoExclusive(True)
        self.create_layout()
        self.connect_signals()

    def create_layout(self) -> None:
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(20, 28, 20, 20)
        sidebar_layout.setSpacing(12)
        sidebar_layout.addWidget(self.brand_label)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(self.modules_button)
        sidebar_layout.addWidget(self.events_button)
        sidebar_layout.addStretch()

    def connect_signals(self) -> None:
        self.modules_button.clicked.connect(self.request_modules)
        self.events_button.clicked.connect(self.request_events)

    def request_modules(self) -> None:
        self.modules_button.setChecked(True)
        self.modules_requested.emit()

    def request_events(self) -> None:
        self.events_button.setChecked(True)
        self.events_requested.emit()
