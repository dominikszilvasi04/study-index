from pathlib import Path

from pytestqt.qtbot import QtBot

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.workspace.module_workspace_page import ModuleWorkspacePage


def test_workspace_loads_and_refreshes_linked_folder_files(
        tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics")
    assert module is not None
    linked_directory = tmp_path / "Files"
    linked_directory.mkdir()
    (linked_directory / "notes.txt").write_text("Notes")
    database.add_linked_folder(module.id, str(linked_directory))
    page = ModuleWorkspacePage(module, database)
    qtbot.addWidget(page)
    assert page.module_name_label.text() == "Mathematics"
    assert page.files_table.topLevelItemCount() == 1
    (linked_directory / "second.pdf").write_text("PDF")
    page.refresh_button.click()
    assert page.files_table.topLevelItemCount() == 2
    with qtbot.waitSignal(page.module_list_requested):
        page.back_button.click()
    database.close()


def test_workspace_displays_folder_scan_errors(tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics")
    assert module is not None
    missing_directory = tmp_path / "Missing"
    database.add_linked_folder(module.id, str(missing_directory))
    page = ModuleWorkspacePage(module, database)
    qtbot.addWidget(page)
    assert page.scan_errors_label.isVisibleTo(page)
    assert str(missing_directory) in page.scan_errors_label.text()
    assert "is not a directory" in page.scan_errors_label.text()
    database.close()
