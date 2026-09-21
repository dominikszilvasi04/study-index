import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

application = QApplication(sys.argv)
application.setApplicationName("StudyIndex")

window = QMainWindow()
window.setWindowTitle("StudyIndex")
window.setCentralWidget(QLabel("No modules yet"))
window.show()

raise SystemExit(application.exec())