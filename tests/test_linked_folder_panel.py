from pathlib import Path
import pytest
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QFileDialog, QMessageBox
from pytestqt.qtbot import QtBot
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.workspace import linked_folder_panel
from study_index.modules.workspace.linked_folder_panel import LinkedFolderPanel


def create_panel(tmp_path: Path, qtbot: QtBot) -> tuple[ModuleDatabase, LinkedFolderPanel]:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics")
    assert module is not None
    panel = LinkedFolderPanel(module, database)
    qtbot.addWidget(panel)
    return database, panel


def test_add_folder_and_duplicate_warning(tmp_path: Path, qtbot: QtBot,
                                          monkeypatch: pytest.MonkeyPatch) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    folder_path = str(tmp_path / "Mathematics")
    warnings: list[str] = []
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args: folder_path)
    monkeypatch.setattr(QMessageBox, "warning", lambda parent, title, message: warnings.append(message))
    with qtbot.waitSignal(panel.folders_changed):
        panel.add_folder()
    assert panel.linked_folders_list.count() == 1
    panel.add_folder()
    assert warnings == ["Folder is already linked"]
    database.close()


def test_cancel_add_folder(tmp_path: Path, qtbot: QtBot,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    monkeypatch.setattr(QFileDialog,
                        "getExistingDirectory",
                        lambda *args: "")
    panel.add_folder()
    assert panel.linked_folders_list.count() == 0
    database.close()


def test_remove_folder_paths(tmp_path: Path, qtbot: QtBot,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    linked_folder = database.add_linked_folder(panel.module.id, "C:/College")
    assert linked_folder is not None
    panel.add_linked_folder_item(linked_folder)
    panel.linked_folders_list.setCurrentRow(0)
    assert panel.remove_folder_button.isEnabled()
    monkeypatch.setattr(QMessageBox,
                        "question",
                        lambda *args: QMessageBox.StandardButton.No)
    panel.remove_folder()
    assert panel.linked_folders_list.count() == 1
    monkeypatch.setattr(QMessageBox,
                        "question",
                        lambda *args: QMessageBox.StandardButton.Yes)
    monkeypatch.setattr(database,
                        "remove_linked_folder",
                        lambda linked_folder_id: False)
    panel.remove_folder()
    assert panel.linked_folders_list.count() == 1
    monkeypatch.setattr(database,
                        "remove_linked_folder",
                        lambda linked_folder_id: True)
    with qtbot.waitSignal(panel.folders_changed):
        panel.remove_folder()
    assert panel.linked_folders_list.count() == 0
    database.close()


def test_selected_folder_is_required(tmp_path: Path, qtbot: QtBot) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    with pytest.raises(RuntimeError, match="folder must be selected"):
        panel.selected_folder_item()
    database.close()


def test_locate_folder_paths(tmp_path: Path, qtbot: QtBot,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    linked_folder = database.add_linked_folder(panel.module.id, "C:/Old")
    assert linked_folder is not None
    panel.add_linked_folder_item(linked_folder)
    panel.linked_folders_list.setCurrentRow(0)
    warnings: list[str] = []
    monkeypatch.setattr(QMessageBox, "warning",
                        lambda parent, title, message: warnings.append(message))
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args: "")
    panel.locate_folder()
    assert panel.selected_folder_item().text() == "C:/Old"
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args: "C:/New")
    monkeypatch.setattr(database, "relocate_linked_folder",
                        lambda linked_folder_id, folder_path: False)
    panel.locate_folder()
    assert warnings == ["Folder is already linked, or link may no longer exist"]
    monkeypatch.setattr(database, "relocate_linked_folder",
                        lambda linked_folder_id, folder_path: True)
    with qtbot.waitSignal(panel.folders_changed):
        panel.locate_folder()
    assert panel.selected_folder_item().text() == "C:/New"
    database.close()


@pytest.mark.parametrize("selected_action", ["Open Folder", "Copy Path"])
def test_folder_actions_and_context_menu(tmp_path: Path, qtbot: QtBot,
                                         monkeypatch: pytest.MonkeyPatch,
                                         selected_action: str) -> None:
    database, panel = create_panel(tmp_path, qtbot)
    linked_folder = database.add_linked_folder(panel.module.id, "C:/College")
    assert linked_folder is not None
    panel.add_linked_folder_item(linked_folder)
    item = panel.linked_folders_list.item(0)
    actions: list[tuple[str, str]] = []

    class FakeMenu:
        def __init__(self, parent: LinkedFolderPanel) -> None:
            pass

        def addAction(self, text: str) -> str:
            return text

        def exec(self, position: QPoint) -> str:
            return selected_action

    monkeypatch.setattr(linked_folder_panel, "QMenu", FakeMenu)
    monkeypatch.setattr(panel.linked_folders_list, "itemAt", lambda position: item)
    monkeypatch.setattr(linked_folder_panel, "open_path",
                        lambda parent, path: actions.append(("open", path)))
    monkeypatch.setattr(linked_folder_panel, "copy_path",
                        lambda path: actions.append(("copy", path)))
    panel.show_context_menu(QPoint())
    expected_action = "open" if selected_action == "Open Folder" else "copy"
    assert actions == [(expected_action, "C:/College")]
    monkeypatch.setattr(panel.linked_folders_list, "itemAt", lambda position: None)
    panel.show_context_menu(QPoint())
    database.close()
