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
    created_stylesheet = None

    def __init__(self, arguments) -> None:
        FakeApplication.created_arguments = arguments
        self.application_name = ""
        self.aboutToQuit = FakeSignal()

    def setApplicationName(self, application_name: str) -> None:
        self.application_name = application_name

    def setStyleSheet(self, stylesheet: str) -> None:
        FakeApplication.created_stylesheet = stylesheet

    def exec(self) -> int:
        return 17


class FakeDatabase:
    created_path = None

    def __init__(self, database_path: Path) -> None:
        FakeDatabase.created_path = database_path

    def close(self) -> None:
        pass


class FakeWindow:
    created_module_database = None
    created_event_database = None

    def __init__(self, module_database: FakeDatabase,
                 event_database: FakeDatabase) -> None:
        FakeWindow.created_module_database = module_database
        FakeWindow.created_event_database = event_database
        self.was_shown = False

    def show(self) -> None:
        self.was_shown = True


def test_main_composes_and_runs_application(tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    data_path = tmp_path / "Data" / "study_index.db"
    monkeypatch.setattr(app, "QApplication", FakeApplication)
    monkeypatch.setattr(app, "ModuleDatabase", FakeDatabase)
    monkeypatch.setattr(app, "EventDatabase", FakeDatabase)
    monkeypatch.setattr(app, "StudyIndexWindow", FakeWindow)
    monkeypatch.setattr(app, "database_path", lambda: data_path)
    assert app.main() == 17
    assert data_path.parent.is_dir()
    assert FakeDatabase.created_path == data_path
    assert isinstance(FakeWindow.created_module_database, FakeDatabase)
    assert isinstance(FakeWindow.created_event_database, FakeDatabase)
    assert FakeApplication.created_stylesheet is not None
    assert "#navigationSidebar" in FakeApplication.created_stylesheet
