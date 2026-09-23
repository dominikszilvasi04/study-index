from datetime import date, time
from pathlib import Path

from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from study_index.events.event_database import EventDatabase
from study_index.events.event_list_page import EventListPage
from study_index.events.models import EventType
from study_index.modules.module_database import ModuleDatabase


def test_event_list_page_shows_empty_and_populated_states(
        tmp_path: Path, qtbot: QtBot) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    event_database = EventDatabase(database_path)
    page = EventListPage(event_database, module_database)
    qtbot.addWidget(page)
    page.show()

    assert page.empty_message.isVisibleTo(page)
    assert not page.events_list.isVisibleTo(page)

    module = module_database.add_module("Machine Learning")
    assert module is not None
    earlier_event = event_database.add_event("Machine Learning Exam",
                                             EventType.EXAM,
                                             date(2026, 12, 14),
                                             time(9, 30),
                                             module.id)
    later_event = event_database.add_event("Project Deadline",
                                           EventType.DEADLINE,
                                           date(2026, 12, 15))
    page.load_events()

    assert page.events_list.isVisibleTo(page)
    assert not page.empty_message.isVisibleTo(page)
    assert page.events_list.count() == 2
    assert page.events_list.item(0).text() == (
        "Machine Learning Exam\nExam · 14 Dec 2026 · 09:30 · Machine Learning"
    )
    assert page.events_list.item(0).data(Qt.ItemDataRole.UserRole) == earlier_event
    assert page.events_list.item(1).text() == (
        "Project Deadline\nDeadline · 15 Dec 2026"
    )
    assert page.events_list.item(1).data(Qt.ItemDataRole.UserRole) == later_event
    event_database.close()
    module_database.close()
