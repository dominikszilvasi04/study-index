import sqlite3
from pathlib import Path
from datetime import date, time
from study_index.events.models import EventType, StudyEvent


class EventDatabase:
    def __init__(self, database_path: Path) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(database_path)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.initialise_tables()

    def add_event(self, title: str, event_type: EventType, event_date: date, event_time: time | None = None,
                  module_id: int | None = None, notes: str = "") -> StudyEvent:
        insert_result = self.connection.execute(
            "INSERT INTO events (title, event_type, event_date, event_time, module_id, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (title,
             event_type.value,
             event_date.isoformat(),
             event_time.isoformat() if event_time is not None else None,
             module_id,
             notes))
        self.connection.commit()
        event_id = insert_result.lastrowid
        if event_id is None:
            raise RuntimeError("SQLite did not return an ID for the new event")
        return StudyEvent(event_id, title, event_type, event_date, event_time, module_id, notes)

    def close(self) -> None:
        self.connection.close()

    # ------------------------------ Utilities ------------------------------

    def initialise_tables(self) -> None:
        self.connection.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, title TEXT NOT NULL, event_type TEXT NOT NULL, event_date TEXT NOT NULL, event_time TEXT, module_id INTEGER, notes TEXT NOT NULL DEFAULT '', FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE SET NULL)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS event_content_links (id INTEGER PRIMARY KEY, event_id INTEGER NOT NULL, content_type TEXT NOT NULL, path TEXT NOT NULL, UNIQUE(event_id, path), FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE)")
        self.connection.commit()