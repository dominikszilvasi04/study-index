from datetime import date, time

from study_index.events.models import (EventContentLink, EventType,
                                       LinkedContentType, StudyEvent)


def test_study_event_stores_schedule_module_and_notes() -> None:
    study_event = StudyEvent(1,
                             "Machine Learning Exam",
                             EventType.EXAM,
                             date(2026, 12, 14),
                             time(9, 30),
                             2,
                             "Revise neural networks and decision trees.")

    assert study_event.title == "Machine Learning Exam"
    assert study_event.event_type == EventType.EXAM
    assert study_event.event_date == date(2026, 12, 14)
    assert study_event.event_time == time(9, 30)
    assert study_event.module_id == 2
    assert study_event.notes.startswith("Revise")


def test_study_event_supports_date_only_events_without_a_module() -> None:
    study_event = StudyEvent(2,
                             "University Closed",
                             EventType.OTHER,
                             date(2026, 12, 21))

    assert study_event.event_time is None
    assert study_event.module_id is None
    assert study_event.notes == ""


def test_event_content_links_distinguish_files_and_folders() -> None:
    file_link = EventContentLink(1,
                                 4,
                                 LinkedContentType.FILE,
                                 "C:/College/Exam Guide.pdf")
    folder_link = EventContentLink(2,
                                   4,
                                   LinkedContentType.FOLDER,
                                   "C:/College/Revision")

    assert file_link.event_id == folder_link.event_id
    assert file_link.content_type == LinkedContentType.FILE
    assert folder_link.content_type == LinkedContentType.FOLDER
