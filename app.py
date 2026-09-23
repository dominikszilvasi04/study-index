import sys
from PySide6.QtWidgets import QApplication
from study_index.config import database_path
from study_index.events.event_database import EventDatabase
from study_index.main_window import StudyIndexWindow
from study_index.modules.module_database import ModuleDatabase
from study_index.style import application_stylesheet

def main() -> int:
    application = QApplication(sys.argv)
    application.setApplicationName("StudyIndex")
    application.setStyleSheet(application_stylesheet())

    module_database_path = database_path()
    module_database_path.parent.mkdir(parents=True, exist_ok=True)

    module_database = ModuleDatabase(module_database_path)
    event_database = EventDatabase(module_database_path)
    application.aboutToQuit.connect(module_database.close)
    application.aboutToQuit.connect(event_database.close)

    window = StudyIndexWindow(module_database, event_database)
    window.show()
    return application.exec()

if __name__ == "__main__":
    raise SystemExit(main())
