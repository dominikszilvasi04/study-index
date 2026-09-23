from datetime import date, time
from pathlib import Path

import pytest

from study_index.events.event_database import EventDatabase
from study_index.events.models import (EventContentLink, EventType,
                                       LinkedContentType, StudyEvent)
from study_index.modules.module_database import ModuleDatabase


def test_add_event_persists_its_details(tmp_path: Path) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    module = module_database.add_module("Machine Learning")
    assert module is not None

    event_database = EventDatabase(database_path)
    study_event = event_database.add_event(
        "Machine Learning Exam",
        EventType.EXAM,
        date(2026, 12, 14),
        time(9, 30),
        module.id,
        "Revise neural networks.")

    assert study_event == StudyEvent(study_event.id,
                                     "Machine Learning Exam",
                                     EventType.EXAM,
                                     date(2026, 12, 14),
                                     time(9, 30),
                                     module.id,
                                     "Revise neural networks.")

    stored_event = event_database.connection.execute(
        "SELECT title, event_type, event_date, event_time, module_id, notes FROM events WHERE id = ?",
        (study_event.id,)).fetchone()

    assert dict(stored_event) == {
        "title": "Machine Learning Exam",
        "event_type": "exam",
        "event_date": "2026-12-14",
        "event_time": "09:30:00",
        "module_id": module.id,
        "notes": "Revise neural networks."
    }

    event_database.close()
    module_database.close()


def test_event_crud_sorting_and_module_removal(tmp_path: Path) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    module = module_database.add_module("Machine Learning")
    assert module is not None
    event_database = EventDatabase(database_path)

    later_event = event_database.add_event("Project Deadline",
                                           EventType.DEADLINE,
                                           date(2026, 12, 15))
    earlier_event = event_database.add_event("Machine Learning Exam",
                                             EventType.EXAM,
                                             date(2026, 12, 14),
                                             time(9, 30),
                                             module.id)
    assert event_database.get_events() == [earlier_event, later_event]

    assert not event_database.update_event(999,
                                           "Missing",
                                           EventType.OTHER,
                                           date(2026, 12, 1))
    assert event_database.update_event(later_event.id,
                                       "Lab Report",
                                       EventType.REPORT,
                                       date(2026, 12, 13),
                                       time(14),
                                       module.id,
                                       "Submit the final report.")
    updated_event = StudyEvent(later_event.id,
                               "Lab Report",
                               EventType.REPORT,
                               date(2026, 12, 13),
                               time(14),
                               module.id,
                               "Submit the final report.")
    assert event_database.get_events() == [updated_event, earlier_event]

    event_database.close()
    event_database = EventDatabase(database_path)
    assert event_database.get_events() == [updated_event, earlier_event]
    assert not event_database.delete_event(999)
    assert event_database.delete_event(earlier_event.id)
    assert event_database.get_events() == [updated_event]

    assert module_database.delete_module(module.id)
    assert event_database.get_events() == [StudyEvent(updated_event.id,
                                                       updated_event.title,
                                                       updated_event.event_type,
                                                       updated_event.event_date,
                                                       updated_event.event_time,
                                                       None,
                                                       updated_event.notes)]
    event_database.close()
    module_database.close()


def test_event_content_links(tmp_path: Path) -> None:
    database_path = tmp_path / "study_index.db"
    module_database = ModuleDatabase(database_path)
    event_database = EventDatabase(database_path)
    study_event = event_database.add_event("Revision",
                                           EventType.OTHER,
                                           date(2026, 12, 10))

    folder_link = event_database.add_event_content_link(
        study_event.id,
        LinkedContentType.FOLDER,
        "C:/College/Revision")
    file_link = event_database.add_event_content_link(
        study_event.id,
        LinkedContentType.FILE,
        "C:/College/Exam Guide.pdf")
    assert folder_link is not None
    assert file_link is not None
    assert event_database.add_event_content_link(
        study_event.id,
        LinkedContentType.FOLDER,
        folder_link.path) is None
    assert event_database.get_event_content_links(study_event.id) == [
        EventContentLink(file_link.id,
                         study_event.id,
                         LinkedContentType.FILE,
                         file_link.path),
        EventContentLink(folder_link.id,
                         study_event.id,
                         LinkedContentType.FOLDER,
                         folder_link.path)
    ]

    assert not event_database.remove_event_content_link(999)
    assert event_database.remove_event_content_link(file_link.id)
    assert event_database.get_event_content_links(study_event.id) == [
        folder_link
    ]
    assert event_database.delete_event(study_event.id)
    assert event_database.get_event_content_links(study_event.id) == []
    event_database.close()
    module_database.close()


class InsertWithoutIdResult:
    rowcount = 1
    lastrowid = None


class ConnectionWithoutInsertIds:
    def execute(self, statement: str,
                parameters: tuple = ()) -> InsertWithoutIdResult:
        return InsertWithoutIdResult()

    def commit(self) -> None:
        pass


def test_missing_sqlite_event_id_is_reported(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    event_database = EventDatabase(tmp_path / "study_index.db")
    event_database.close()
    monkeypatch.setattr(event_database,
                        "connection",
                        ConnectionWithoutInsertIds())

    with pytest.raises(RuntimeError, match="ID for the new event"):
        event_database.add_event("Exam",
                                 EventType.EXAM,
                                 date(2026, 12, 14))
    with pytest.raises(RuntimeError, match="ID for the new event content link"):
        event_database.add_event_content_link(1,
                                              LinkedContentType.FILE,
                                              "C:/College/Guide.pdf")
