from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QLabel,
                               QLineEdit, QVBoxLayout)

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import LinkedFolder, Module
from study_index.modules.workspace.file_finder import FileFinder
from study_index.modules.workspace.module_files_table import ModuleFilesTable


class ModuleFilesPanel(QFrame):
    title_label: QLabel
    file_count_label: QLabel
    file_search: QLineEdit
    file_type_filter: QComboBox
    files_table: ModuleFilesTable
    scan_errors_label: QLabel

    def __init__(self, module: Module,
                 module_database: ModuleDatabase) -> None:
        super().__init__()
        self.setObjectName("filesPanel")
        self.module = module
        self.module_database = module_database
        self.create_widgets()
        self.create_layout()
        self.connect_signals()
        self.refresh_files()

    def create_widgets(self) -> None:
        self.title_label = QLabel("Files")
        self.title_label.setObjectName("workspacePanelTitle")
        self.file_count_label = QLabel()
        self.file_count_label.setObjectName("workspaceCountLabel")
        self.file_search = QLineEdit()
        self.file_search.setPlaceholderText("Search for files")
        self.file_search.setClearButtonEnabled(True)
        self.file_type_filter = self.create_file_type_filter()
        self.files_table = ModuleFilesTable()
        self.scan_errors_label = QLabel()
        self.scan_errors_label.setObjectName("scanErrorsLabel")
        self.scan_errors_label.setWordWrap(True)
        self.scan_errors_label.hide()

    @staticmethod
    def create_file_type_filter() -> QComboBox:
        file_type_filter = QComboBox()
        file_type_filter.addItem("All file types", None)
        file_type_filter.addItem("PDF", (".pdf",))
        file_type_filter.addItem("Word", (".doc", ".docx"))
        file_type_filter.addItem("PowerPoint", (".ppt", ".pptx"))
        file_type_filter.addItem("Text", (".txt",))
        file_type_filter.addItem("HTML", (".html",))
        return file_type_filter

    def create_layout(self) -> None:
        panel_layout = QVBoxLayout(self)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)
        panel_layout.addLayout(self.create_header_layout())
        panel_layout.addLayout(self.create_filter_layout())
        panel_layout.addWidget(self.files_table, 1)
        panel_layout.addWidget(self.scan_errors_label)

    def create_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(8)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.file_count_label)
        header_layout.addStretch()
        return header_layout

    def create_filter_layout(self) -> QHBoxLayout:
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(18, 14, 18, 14)
        filter_layout.setSpacing(10)
        filter_layout.addWidget(self.file_search)
        filter_layout.addWidget(self.file_type_filter)
        return filter_layout

    def connect_signals(self) -> None:
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
        self.file_count_label.setText(f"({self.files_table.topLevelItemCount()})")
        self.apply_file_filters()

    def load_linked_folder_files(self, linked_folder: LinkedFolder) -> None:
        file_finder = FileFinder(linked_folder.path)
        for file_metadata in file_finder.find_files():
            self.files_table.add_file(linked_folder.path, file_metadata)
