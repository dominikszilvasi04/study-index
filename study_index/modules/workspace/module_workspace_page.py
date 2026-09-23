from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.models import Module
from study_index.modules.workspace.linked_folder_panel import LinkedFolderPanel
from study_index.modules.workspace.module_files_panel import ModuleFilesPanel
from study_index.modules.workspace.module_workspace_header import ModuleWorkspaceHeader


class ModuleWorkspacePage(QWidget):
    module_list_requested = Signal()

    def __init__(self, module: Module,
                 module_database: ModuleDatabase) -> None:
        super().__init__()
        self.setObjectName("moduleWorkspacePage")
        self.workspace_header = ModuleWorkspaceHeader(module)
        self.linked_folder_panel = LinkedFolderPanel(module, module_database)
        self.files_panel = ModuleFilesPanel(module, module_database)
        self.create_layout()
        self.connect_signals()

    def create_layout(self) -> None:
        workspace_layout = QHBoxLayout()
        workspace_layout.setSpacing(18)
        workspace_layout.addWidget(self.linked_folder_panel)
        workspace_layout.addWidget(self.files_panel, 1)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(30, 24, 30, 30)
        page_layout.setSpacing(18)
        page_layout.addWidget(self.workspace_header)
        page_layout.addLayout(workspace_layout, 1)

    def connect_signals(self) -> None:
        self.workspace_header.module_list_requested.connect(self.module_list_requested.emit)
        self.workspace_header.refresh_requested.connect(self.files_panel.refresh_files)
        self.linked_folder_panel.folders_changed.connect(self.files_panel.refresh_files)
