from pathlib import Path

import pytest
from pytestqt.qtbot import QtBot

from study_index.main_window import StudyIndexWindow
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.workspace.module_workspace_page import ModuleWorkspacePage


def test_window_navigates_between_module_list_and_workspace(tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics")
    assert module is not None
    window = StudyIndexWindow(database)
    qtbot.addWidget(window)
    window.show_module_workspace(module)
    assert isinstance(window.page_stack.currentWidget(), ModuleWorkspacePage)
    assert window.page_stack.count() == 2
    window.show_module_list()
    assert window.page_stack.currentWidget() is window.module_list_page
    assert window.page_stack.count() == 1
    database.close()


def test_show_module_list_requires_current_page(tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    window = StudyIndexWindow(database)
    qtbot.addWidget(window)
    window.page_stack.removeWidget(window.module_list_page)
    with pytest.raises(RuntimeError, match="does not have a current page"):
        window.show_module_list()
    database.close()
