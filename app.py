import sys
from PySide6.QtWidgets import QApplication
from study_index.main_window import StudyIndexWindow

def main():
    application = QApplication(sys.argv)
    application.setApplicationName("StudyIndex")
    window = StudyIndexWindow()
    window.show()
    return application.exec()

if __name__ == "__main__":
    raise SystemExit(main())
