import sys
from PySide6.QtWidgets import QApplication
from study_index.config import database_path
from study_index.main_window import StudyIndexWindow
from study_index.modules.modules_repository import ModuleRepository

def main():
    application = QApplication(sys.argv)
    application.setApplicationName("StudyIndex")

    module_database_path = database_path()
    module_database_path.parent.mkdir(parents=True, exist_ok=True)

    module_repository = ModuleRepository(module_database_path)
    application.aboutToQuit.connect(module_repository.close)

    window = StudyIndexWindow(module_repository)
    window.show()
    return application.exec()

if __name__ == "__main__":
    raise SystemExit(main())
