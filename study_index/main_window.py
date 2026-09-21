from PySide6.QtWidgets import QMainWindow
from study_index.modules_page import ModulesPage


class StudyIndexWindow(QMainWindow):
    def __init__(self, module_repository):
        super().__init__()
        self.setWindowTitle("Study Index")
        self.modules_page = ModulesPage(module_repository)
        self.setCentralWidget(self.modules_page)
