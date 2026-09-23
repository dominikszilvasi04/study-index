from pathlib import Path

import pytest
from pytestqt.qtbot import QtBot

from study_index.events.event_database import EventDatabase
from study_index.main_window import StudyIndexWindow
from study_index.modules.module_database import ModuleDatabase
from study_index.modules.workspace.module_workspace_page import ModuleWorkspacePage


def test_window_navigates_between_module_list_and_workspace(
        tmp_path: Path, qtbot: QtBot) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    event_database = EventDatabase(database_path)
    module = module_database.add_module("Mathematics")
    assert module is not None
    window = StudyIndexWindow(module_database, event_database)
    qtbot.addWidget(window)
    assert window.windowTitle() == "StudyIndex"
    assert window.minimumWidth() == 900
    assert window.minimumHeight() == 600
    assert window.navigation_sidebar.minimumWidth() == 200
    assert window.navigation_sidebar.modules_button.isChecked()
    window.show_module_workspace(module)
    assert isinstance(window.page_stack.currentWidget(), ModuleWorkspacePage)
    assert window.page_stack.count() == 3
    window.navigation_sidebar.modules_button.click()
    assert window.page_stack.currentWidget() is window.module_list_page
    assert window.page_stack.count() == 2
    assert window.navigation_sidebar.modules_button.isChecked()
    window.navigation_sidebar.events_button.click()
    assert window.page_stack.currentWidget() is window.event_list_page
    assert window.page_stack.count() == 2
    assert window.navigation_sidebar.events_button.isChecked()
    window.show_module_workspace(module)
    window.navigation_sidebar.events_button.click()
    assert window.page_stack.currentWidget() is window.event_list_page
    assert window.page_stack.count() == 2
    event_database.close()
    module_database.close()


def test_show_module_list_requires_current_page(tmp_path: Path, qtbot: QtBot) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    event_database = EventDatabase(database_path)
    window = StudyIndexWindow(module_database, event_database)
    qtbot.addWidget(window)
    window.page_stack.removeWidget(window.module_list_page)
    window.page_stack.removeWidget(window.event_list_page)
    with pytest.raises(RuntimeError, match="does not have a current page"):
        window.show_module_list()
    event_database.close()
    module_database.close()
