import sqlite3
from pathlib import Path
from datetime import date, time
from study_index.events.models import EventContentLink, EventType, LinkedContentType, StudyEvent


class EventDatabase:
    def __init__(self, database_path: Path) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
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
        return StudyEvent(id=event_id, title=title, event_type=event_type, event_date=event_date,
                          event_time=event_time, module_id=module_id, notes=notes)

    def get_events(self) -> list[StudyEvent]:
        rows = self.connection.execute("SELECT id, title, event_type, event_date, event_time, module_id, notes FROM events ORDER BY event_date, event_time, title COLLATE NOCASE")
        return [self.study_event_from_row(row) for row in rows]

    def update_event(self, event_id: int, title: str, event_type: EventType, event_date: date,
                     event_time: time | None = None, module_id: int | None = None, notes: str = "") -> bool:
        update_result = self.connection.execute(
            "UPDATE events SET title = ?, event_type = ?, event_date = ?, event_time = ?, module_id = ?, notes = ? WHERE id = ?",
            (title,
             event_type.value,
             event_date.isoformat(),
             event_time.isoformat() if event_time is not None else None,
             module_id,
             notes,
             event_id))
        self.connection.commit()
        return update_result.rowcount == 1

    def delete_event(self, event_id: int) -> bool:
        delete_result = self.connection.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.connection.commit()
        return delete_result.rowcount == 1

    def add_event_content_link(self, event_id: int, content_type: LinkedContentType,
                               path: str) -> EventContentLink | None:
        insert_result = self.connection.execute(
            "INSERT OR IGNORE INTO event_content_links (event_id, content_type, path) VALUES (?, ?, ?)",
            (event_id, content_type.value, path))
        self.connection.commit()
        if insert_result.rowcount == 0:
            return None
        content_link_id = insert_result.lastrowid
        if content_link_id is None:
            raise RuntimeError("SQLite did not return an ID for the new event content link")
        return EventContentLink(id=content_link_id, event_id=event_id, content_type=content_type, path=path)

    def get_event_content_links(self, event_id: int) -> list[EventContentLink]:
        rows = self.connection.execute("SELECT id, event_id, content_type, path FROM event_content_links WHERE event_id = ? ORDER BY path COLLATE NOCASE",
                                       (event_id,))
        return [self.event_content_link_from_row(row) for row in rows]

    def remove_event_content_link(self, content_link_id: int) -> bool:
        delete_result = self.connection.execute("DELETE FROM event_content_links WHERE id = ?", (content_link_id,))
        self.connection.commit()
        return delete_result.rowcount == 1

    def close(self) -> None:
        self.connection.close()

    # ------------------------------ Utilities ------------------------------

    def initialise_tables(self) -> None:
        self.connection.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, title TEXT NOT NULL, event_type TEXT NOT NULL, event_date TEXT NOT NULL, event_time TEXT, module_id INTEGER, notes TEXT NOT NULL DEFAULT '', FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE SET NULL)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS event_content_links (id INTEGER PRIMARY KEY, event_id INTEGER NOT NULL, content_type TEXT NOT NULL, path TEXT NOT NULL, UNIQUE(event_id, path), FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE)")
        self.connection.commit()

    @staticmethod
    def study_event_from_row(row: sqlite3.Row) -> StudyEvent:
        stored_event_time = None
        if row["event_time"] is not None:
            stored_event_time = time.fromisoformat(row["event_time"])
        return StudyEvent(id=row["id"], title=row["title"], event_type=EventType(row["event_type"]),
                          event_date=date.fromisoformat(row["event_date"]), event_time=stored_event_time,
                          module_id=row["module_id"], notes=row["notes"])

    @staticmethod
    def event_content_link_from_row(row: sqlite3.Row) -> EventContentLink:
        return EventContentLink(id=row["id"],
                                event_id=row["event_id"],
                                content_type=LinkedContentType(row["content_type"]),
                                path=row["path"])
