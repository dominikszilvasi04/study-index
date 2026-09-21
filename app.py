import sys
from PySide6.QtWidgets import QApplication

def main():
    application = QApplication(sys.argv)
    application.setApplicationName("StudyIndex")
    return application.exec()

if __name__ == "__main__":
    raise SystemExit(main())