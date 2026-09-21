from PySide6.QtWidgets import QMainWindow, QStackedWidget
from study_index.modules.module_list_page import ModuleListPage
from study_index.modules.module_workspace_page import ModuleWorkspacePage


class StudyIndexWindow(QMainWindow):
    def __init__(self, module_database):
        super().__init__()
        self.module_database = module_database
        self.setWindowTitle("Study Index")
        self.module_list_page = ModuleListPage(module_database)
        self.module_list_page.module_open_requested.connect(self.show_module_workspace)
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(self.module_list_page)
        self.setCentralWidget(self.page_stack)

    def show_module_workspace(self, module) -> None:
        workspace_page = ModuleWorkspacePage(module, self.module_database)
        workspace_page.module_list_requested.connect(self.show_module_list)
        self.page_stack.addWidget(workspace_page)
        self.page_stack.setCurrentWidget(workspace_page)

    def show_module_list(self) -> None:
        workspace_page = self.page_stack.currentWidget()
        self.page_stack.setCurrentWidget(self.module_list_page)
        self.page_stack.removeWidget(workspace_page)
        workspace_page.deleteLater()
