from pathlib import Path
import pytest
import app


class FakeSignal:
    def __init__(self) -> None:
        self.connected_method = None

    def connect(self, method) -> None:
        self.connected_method = method


class FakeApplication:
    created_arguments = None

    def __init__(self, arguments) -> None:
        FakeApplication.created_arguments = arguments
        self.application_name = ""
        self.aboutToQuit = FakeSignal()

    def setApplicationName(self, application_name: str) -> None:
        self.application_name = application_name

    def exec(self) -> int:
        return 17


class FakeDatabase:
    created_path = None

    def __init__(self, database_path: Path) -> None:
        FakeDatabase.created_path = database_path

    def close(self) -> None:
        pass


class FakeWindow:
    created_database = None

    def __init__(self, database: FakeDatabase) -> None:
        FakeWindow.created_database = database
        self.was_shown = False

    def show(self) -> None:
        self.was_shown = True


def test_main_composes_and_runs_application(tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    data_path = tmp_path / "Data" / "study_index.db"
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "ModuleDatabase", FakeDatabase)
    monkeypatch.setattr(app, "StudyIndexWindow", FakeWindow)
    monkeypatch.setattr(app, "database_path", lambda: data_path)
    assert app.main() == 17
    assert data_path.parent.is_dir()
    assert FakeDatabase.created_path == data_path
    assert isinstance(FakeWindow.created_database, FakeDatabase)
