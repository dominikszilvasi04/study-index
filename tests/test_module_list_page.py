from pathlib import Path

import pytest
from PySide6.QtWidgets import QDialog, QMessageBox
from pytestqt.qtbot import QtBot

from study_index.modules.module_database import ModuleDatabase
from study_index.modules.module_list_page import ModuleListPage
from study_index.modules.module_details_form import ModuleDetailsForm


def test_page_loads_modules_and_emits_selected_module(tmp_path: Path,
                                                      qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    module = database.add_module("Mathematics", "MATH101", "Semester 1")
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
        page.open_module_button_clicked()
    assert signal.args == [module]
    with qtbot.waitSignal(page.module_open_requested) as signal:
        page.modules_list.itemActivated.emit(page.modules_list.item(0))
    assert signal.args == [module]
    database.close()


def test_add_and_edit_module(tmp_path: Path, qtbot: QtBot,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    page = ModuleListPage(database)
    qtbot.addWidget(page)
    responses = iter([("  Mathematics  ", " MATH101 ", " Semester 1 "),
                      ("Physics", "PHY101", "Semester 2")])

    def complete_form(form):
        if form.windowTitle() == "Edit Module":
            assert form.name_input.text() == "Mathematics"
            assert form.code_input.text() == "MATH101"
            assert form.term_input.text() == "Semester 1"
        name, code, term = next(responses)
        form.name_input.setText(name)
        form.code_input.setText(code)
        form.term_input.setText(term)
        form.accept()
        return form.result()

    monkeypatch.setattr(ModuleDetailsForm, "exec", complete_form)
    page.add_module()
    assert page.modules_list.item(0).text() == "Mathematics\nMATH101 · Semester 1"
    page.modules_list.setCurrentRow(0)
    page.edit_module()
    assert page.modules_list.item(0).text() == "Physics\nPHY101 · Semester 2"
    saved_module = database.get_modules()[0]
    assert (saved_module.name, saved_module.code, saved_module.term) == ("Physics", "PHY101", "Semester 2")
    with qtbot.waitSignal(page.module_open_requested) as signal:
        page.open_module_button_clicked()
    assert signal.args == [saved_module]
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
    monkeypatch.setattr(ModuleDetailsForm, "exec", lambda self: QDialog.DialogCode.Rejected)
    assert page.request_module_details("Add Module") is None
    form = ModuleDetailsForm(page, "Add Module")
    qtbot.addWidget(form)
    form.name_input.setText("   ")
    form.accept()
    assert form.result() == QDialog.DialogCode.Rejected
    assert warnings == ["Module name cannot be empty"]
    monkeypatch.setattr(page, "request_module_details", lambda *args: ("Mathematics", "", ""))
    page.add_module()
    assert warnings[-1] == "Module name already exists"
    page.modules_list.setCurrentRow(0)
    monkeypatch.setattr(page, "request_module_details", lambda *args: ("Physics", "", ""))
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
                        "request_module_details",
                        lambda title, module=None: None)
    page.add_module()
    page.edit_module()
    assert page.modules_list.count() == 1
    assert page.modules_list.item(0).text() == "Mathematics"
    database.close()

def test_module_search_filters_name_code_and_term(
        tmp_path: Path, qtbot: QtBot) -> None:
    database = ModuleDatabase(tmp_path / "study_index.db")
    database.add_module("Mathematics", "MATH101", "Semester 1")
    database.add_module("Physics", "PHY101", "Semester 2")
    page = ModuleListPage(database)
    qtbot.addWidget(page)

    page.search_input.setText("math101")
    assert not page.modules_list.item(0).isHidden()
    assert page.modules_list.item(1).isHidden()

    page.search_input.setText("semester 2")
    assert page.modules_list.item(0).isHidden()
    assert not page.modules_list.item(1).isHidden()

    page.search_input.setText("missing")
    assert page.empty_message.isVisibleTo(page)
    assert page.empty_message.text() == "No modules match your search."

    page.search_input.clear()
    assert page.modules_list.isVisibleTo(page)
    assert not page.empty_message.isVisibleTo(page)
    database.close()
