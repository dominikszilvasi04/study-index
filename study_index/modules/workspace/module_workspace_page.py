from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QWidget)

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
        self.setObjectName("moduleWorkspacePage")
        self.module = module
        self.module_database = module_database
        self.module_name_label = QLabel(self.module.name)
        self.module_name_label.setObjectName("moduleNameLabel")
        self.module_details_label = QLabel(" · ".join(value for value in (module.code, module.term) if value))
        self.module_details_label.setObjectName("moduleDetailsLabel")
        self.linked_folder_panel = LinkedFolderPanel(self.module, self.module_database)
        self.files_label = QLabel("Files")
        self.files_label.setObjectName("workspacePanelTitle")
        self.files_count_label = QLabel()
        self.files_count_label.setObjectName("workspaceCountLabel")
        self.file_search = QLineEdit()
        self.file_search.setPlaceholderText("Search for files")
        self.file_search.setClearButtonEnabled(True)
        self.file_type_filter = QComboBox()
        self.file_type_filter.addItem("All file types", None)
        self.file_type_filter.addItem("PDF", (".pdf",))
        self.file_type_filter.addItem("Word", (".doc", ".docx"))
        self.file_type_filter.addItem("PowerPoint", (".ppt", ".pptx"))
        self.file_type_filter.addItem("Text", (".txt",))
        self.file_type_filter.addItem("HTML", (".html",))
        self.files_table = ModuleFilesTable()
        self.refresh_button = QPushButton("Refresh")
        self.back_button = QPushButton("←  Back to Modules")
        self.back_button.setObjectName("workspaceBackButton")
        self.scan_errors_label = QLabel()
        self.scan_errors_label.setObjectName("scanErrorsLabel")
        self.scan_errors_label.setWordWrap(True)
        self.scan_errors_label.hide()
        self.create_layout()
        self.module_details_label.setVisible(bool(module.code or module.term))
        self.connect_signals()
        self.refresh_files()

    def create_layout(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(30, 24, 30, 30)
        page_layout.setSpacing(18)
        page_layout.addWidget(self.back_button, 0)

        module_heading_layout = QVBoxLayout()
        module_heading_layout.setSpacing(4)
        module_heading_layout.addWidget(self.module_name_label)
        module_heading_layout.addWidget(self.module_details_label)

        header_layout = QHBoxLayout()
        header_layout.addLayout(module_heading_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        page_layout.addLayout(header_layout)

        files_panel = QFrame()
        files_panel.setObjectName("filesPanel")
        files_panel_layout = QVBoxLayout(files_panel)
        files_panel_layout.setContentsMargins(0, 0, 0, 0)
        files_panel_layout.setSpacing(0)

        files_header_layout = QHBoxLayout()
        files_header_layout.setContentsMargins(18, 14, 18, 14)
        files_header_layout.setSpacing(8)
        files_header_layout.addWidget(self.files_label)
        files_header_layout.addWidget(self.files_count_label)
        files_header_layout.addStretch()
        files_panel_layout.addLayout(files_header_layout)

        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(18, 14, 18, 14)
        filter_layout.setSpacing(10)
        filter_layout.addWidget(self.file_search)
        filter_layout.addWidget(self.file_type_filter)
        files_panel_layout.addLayout(filter_layout)
        files_panel_layout.addWidget(self.files_table, 1)
        files_panel_layout.addWidget(self.scan_errors_label)

        workspace_layout = QHBoxLayout()
        workspace_layout.setSpacing(18)
        workspace_layout.addWidget(self.linked_folder_panel)
        workspace_layout.addWidget(files_panel, 1)
        page_layout.addLayout(workspace_layout, 1)

    def connect_signals(self) -> None:
        self.linked_folder_panel.folders_changed.connect(self.refresh_files)
        self.refresh_button.clicked.connect(self.refresh_files)
        self.back_button.clicked.connect(self.module_list_requested.emit)
        self.file_search.textChanged.connect(self.apply_file_filters)
        self.file_type_filter.currentIndexChanged.connect(self.apply_file_filters)

    def apply_file_filters(self) -> None:
        search_text = self.file_search.text()
        selected_extensions = self.file_type_filter.currentData()
        self.files_table.filter_files(search_text, selected_extensions)

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
        file_count = self.files_table.topLevelItemCount()
        self.files_count_label.setText(f"({file_count})")
        self.apply_file_filters()

    def load_linked_folder_files(self, linked_folder: LinkedFolder) -> None:
        file_finder = FileFinder(linked_folder.path)

        for file_metadata in file_finder.find_files():
            self.files_table.add_file(linked_folder.path, file_metadata)
