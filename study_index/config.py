from pathlib import Path
from PySide6.QtCore import QStandardPaths


def application_data_directory() -> Path:
    data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
    return Path(data_path)


def database_path() -> Path:
    return application_data_directory() / "study_index.db"
