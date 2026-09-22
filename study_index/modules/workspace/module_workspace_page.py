from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import LinkedFolder, Module
from study_index.modules.workspace.file_finder import FileFinder
from study_index.modules.workspace.linked_folder_panel import LinkedFolderPanel
from study_index.modules.workspace.module_files_table import ModuleFilesTable


class ModuleWorkspacePage(QWidget):
    module_list_requested = Signal()

    def __init__(self, module: Module,
                 module_database: ModuleDatabase) -> None:
        super().__init__()
        self.module = module
        self.module_database = module_database
        self.module_name_label = QLabel(self.module.name)
        self.linked_folder_panel = LinkedFolderPanel(self.module,
                                                     self.module_database)
        self.files_label = QLabel("Files")
        self.files_table = ModuleFilesTable()
        self.refresh_button = QPushButton("Refresh")
        self.back_button = QPushButton("Back to Modules")
        self.scan_errors_label = QLabel()
        self.scan_errors_label.setWordWrap(True)
        self.scan_errors_label.hide()
        self.create_layout()
        self.connect_signals()
        self.refresh_files()

    def create_layout(self) -> None:
        page_layout = QVBoxLayout()
        page_layout.addWidget(self.module_name_label)
        page_layout.addWidget(self.linked_folder_panel)
        page_layout.addWidget(self.files_label)
        page_layout.addWidget(self.files_table)
        page_layout.addWidget(self.scan_errors_label)
        page_layout.addWidget(self.refresh_button)
        page_layout.addWidget(self.back_button)
        self.setLayout(page_layout)

    def connect_signals(self) -> None:
        self.linked_folder_panel.folders_changed.connect(self.refresh_files)
        self.refresh_button.clicked.connect(self.refresh_files)
        self.back_button.clicked.connect(self.module_list_requested.emit)

    def refresh_files(self) -> None:
        self.files_table.clear()
        errors = []
        for linked_folder in self.module_database.get_linked_folders(self.module.id):
            try:
                self.load_linked_folder_files(linked_folder)
            except OSError as error:
                errors.append(f"{linked_folder.path}: {error}")
        self.scan_errors_label.setText("\n".join(errors))
        self.scan_errors_label.setVisible(bool(errors))

    def load_linked_folder_files(self, linked_folder: LinkedFolder) -> None:
        file_finder = FileFinder(linked_folder.path)

        for file_metadata in file_finder.find_files():
            self.files_table.add_file(linked_folder.path, file_metadata)
