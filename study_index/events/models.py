from dataclasses import dataclass
from datetime import date, time
from enum import StrEnum


class EventType(StrEnum):
    EXAM = "exam"
    QUIZ = "quiz"
    LAB = "lab"
    REPORT = "report"
    ASSIGNMENT = "assignment"
    DEADLINE = "deadline"
    OTHER = "other"


class LinkedContentType(StrEnum):
    FILE = "file"
    FOLDER = "folder"


@dataclass(frozen=True)
class StudyEvent:
    id: int
    title: str
    event_type: EventType
    event_date: date
    event_time: time | None = None
    module_id: int | None = None
    notes: str = ""


@dataclass(frozen=True)
class EventContentLink:
    id: int
    event_id: int
    content_type: LinkedContentType
    path: str
