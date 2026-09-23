from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.module_list_page import ModuleListPage
from study_index.modules.models import Module
from study_index.modules.workspace.module_workspace_page import ModuleWorkspacePage
from study_index.navigation_sidebar import NavigationSidebar


class StudyIndexWindow(QMainWindow):
    def __init__(self, module_database: ModuleDatabase) -> None:
        super().__init__()
        self.module_database = module_database
        self.setWindowTitle("StudyIndex")
        self.setMinimumSize(900, 600)
        self.navigation_sidebar = NavigationSidebar()
        self.module_list_page = ModuleListPage(module_database)
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(self.module_list_page)
        self.create_layout()
        self.connect_signals()

    def create_layout(self) -> None:
        window_content = QWidget()
        window_layout = QHBoxLayout(window_content)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.addWidget(self.navigation_sidebar)
        window_layout.addWidget(self.page_stack)
        self.setCentralWidget(window_content)

    def connect_signals(self) -> None:
        self.navigation_sidebar.modules_requested.connect(self.show_module_list)
        self.module_list_page.module_open_requested.connect(self.show_module_workspace)

    def show_module_workspace(self, module: Module) -> None:
        workspace_page = ModuleWorkspacePage(module, self.module_database)
        workspace_page.module_list_requested.connect(self.show_module_list)
        self.page_stack.addWidget(workspace_page)
        self.page_stack.setCurrentWidget(workspace_page)

    def show_module_list(self) -> None:
        workspace_page = self.page_stack.currentWidget()
        if workspace_page is None:
            raise RuntimeError("The page stack does not have a current page")
        if workspace_page is self.module_list_page:
            return
        self.page_stack.setCurrentWidget(self.module_list_page)
        self.page_stack.removeWidget(workspace_page)
        workspace_page.deleteLater()
