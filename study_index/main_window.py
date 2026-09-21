from PySide6.QtWidgets import QMainWindow
from study_index.modules_page import ModulesPage

class StudyIndexWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Index")
        self.modules_page = ModulesPage()
        self.setCentralWidget(self.modules_page)