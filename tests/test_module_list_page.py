from pathlib import Path

import pytest
from PySide6.QtWidgets import QInputDialog, QMessageBox
from pytestqt.qtbot import QtBot

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.module_list_page import ModuleListPage


def test_page_loads_modules_and_emits_selected_module(tmp_path: Path,
                                                      qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics")
    assert module is not None
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    assert page.modules_list.count() == 1
    assert not page.empty_message.isVisible()
    assert not page.open_module_button.isEnabled()
    page.modules_list.setCurrentRow(0)
    assert page.open_module_button.isEnabled()
    assert page.edit_module_button.isEnabled()
    assert page.delete_module_button.isEnabled()
    with qtbot.waitSignal(page.module_open_requested) as signal:
        page.request_module_open()
    assert signal.args == [module]
    database.close()


def test_add_and_edit_module(tmp_path: Path, qtbot: QtBot,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    responses = iter([("  Mathematics  ", True), ("Physics", True)])
    monkeypatch.setattr(QInputDialog,
                        "getText",
                        lambda *args, **kwargs: next(responses))
    page.add_module()
    assert page.modules_list.item(0).text() == "Mathematics"
    page.modules_list.setCurrentRow(0)
    page.edit_module()
    assert page.modules_list.item(0).text() == "Physics"
    assert database.get_modules()[0].name == "Physics"
    database.close()


def test_module_name_rejections_show_expected_behaviour(
        tmp_path: Path, qtbot: QtBot,
        monkeypatch: pytest.MonkeyPatch) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    database.add_module("Mathematics")
    database.add_module("Physics")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    warnings: list[str] = []
    monkeypatch.setattr(QMessageBox,
                        "warning",
                        lambda parent, title, message: warnings.append(message))
    monkeypatch.setattr(QInputDialog,
                        "getText",
                        lambda *args, **kwargs: ("", False))
    assert page.request_module_name("Add Module") is None
    monkeypatch.setattr(QInputDialog,
                        "getText",
                        lambda *args, **kwargs: ("   ", True))
    assert page.request_module_name("Add Module") is None
    assert warnings == ["Module name cannot be empty"]
    monkeypatch.setattr(QInputDialog,
                        "getText",
                        lambda *args, **kwargs: ("Mathematics", True))
    page.add_module()
    assert warnings[-1] == "Module name already exists"
    page.modules_list.setCurrentRow(0)
    monkeypatch.setattr(QInputDialog,
                        "getText",
                        lambda *args, **kwargs: ("Physics", True))
    page.edit_module()
    assert warnings[-1] == "Module name already exists"
    database.close()


def test_delete_module_confirmation_and_database_failure(
        tmp_path: Path, qtbot: QtBot,
        monkeypatch: pytest.MonkeyPatch) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    database.add_module("Mathematics")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    page.modules_list.setCurrentRow(0)
    monkeypatch.setattr(QMessageBox,
                        "question",
                        lambda *args: QMessageBox.StandardButton.No)
    page.delete_module()
    assert page.modules_list.count() == 1
    monkeypatch.setattr(QMessageBox,
                        "question",
                        lambda *args: QMessageBox.StandardButton.Yes)
    monkeypatch.setattr(database, "delete_module", lambda module_id: False)
    page.delete_module()
    assert page.modules_list.count() == 1
    monkeypatch.setattr(database, "delete_module", lambda module_id: True)
    page.delete_module()
    assert page.modules_list.count() == 0
    database.close()


def test_selected_module_is_required(tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    with pytest.raises(RuntimeError, match="module must be selected"):
        page.selected_module_item()
    database.close()


def test_cancelled_add_and_edit_leave_modules_unchanged(
        tmp_path: Path, qtbot: QtBot,
        monkeypatch: pytest.MonkeyPatch) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    database.add_module("Mathematics")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    page.modules_list.setCurrentRow(0)
    monkeypatch.setattr(page,
                        "request_module_name",
                        lambda title, current_name="": None)
    page.add_module()
    page.edit_module()
    assert page.modules_list.count() == 1
    assert page.modules_list.item(0).text() == "Mathematics"
    database.close()
