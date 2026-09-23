from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from study_index.events.event_database import EventDatabase
from study_index.events.event_list_page import EventListPage
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.module_list_page import ModuleListPage
from study_index.modules.models import Module
from study_index.modules.workspace.module_workspace_page import ModuleWorkspacePage
from study_index.navigation_sidebar import NavigationSidebar


class StudyIndexWindow(QMainWindow):
    def __init__(self, module_database: ModuleDatabase, event_database: EventDatabase) -> None:
        super().__init__()
        self.module_database = module_database
        self.event_database = event_database
        self.setWindowTitle("StudyIndex")
        self.setMinimumSize(900, 600)
        self.navigation_sidebar = NavigationSidebar()
        self.module_list_page = ModuleListPage(module_database)
        self.event_list_page = EventListPage(event_database, module_database)
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(self.module_list_page)
        self.page_stack.addWidget(self.event_list_page)
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
        self.navigation_sidebar.events_requested.connect(self.show_events)
        self.module_list_page.module_open_requested.connect(self.show_module_workspace)

    def show_module_workspace(self, module: Module) -> None:
        workspace_page = ModuleWorkspacePage(module, self.module_database)
        workspace_page.module_list_requested.connect(self.show_module_list)
        self.page_stack.addWidget(workspace_page)
        self.page_stack.setCurrentWidget(workspace_page)

    def show_module_list(self) -> None:
        self.show_persistent_page(self.module_list_page)

    def show_events(self) -> None:
        self.event_list_page.load_events()
        self.show_persistent_page(self.event_list_page)

    # ------------------------------ Utilities ------------------------------

    def show_persistent_page(self, page: QWidget) -> None:
        current_page = self.page_stack.currentWidget()
        if current_page is None:
            raise RuntimeError("The page stack does not have a current page")
        self.page_stack.setCurrentWidget(page)
        if isinstance(current_page, ModuleWorkspacePage):
            self.page_stack.removeWidget(current_page)
            current_page.deleteLater()
