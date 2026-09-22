from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget


def open_path(parent: QWidget, path: str) -> None:
    if not QDesktopServices.openUrl(QUrl.fromLocalFile(path)):
        QMessageBox.warning(parent, "Cannot Open", f"Could not open:\n{path}")


def copy_path(path: str) -> None:
    QApplication.clipboard().setText(path)
