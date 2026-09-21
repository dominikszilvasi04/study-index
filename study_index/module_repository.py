import sqlite3
from pathlib import Path


class ModuleRepository:
    def __init__(self, database_path: Path):
        self.connection = sqlite3.connect(database_path)
        self.connection.execute("CREATE TABLE IF NOT EXISTS modules (name TEXT NOT NULL UNIQUE)")

    def add(self, name: str) -> bool:
        cursor = self.connection.execute("INSERT OR IGNORE INTO modules VALUES (?)", (name,))
        self.connection.commit()
        return cursor.rowcount == 1

    def names(self) -> list[str]:
        rows = self.connection.execute("SELECT name FROM modules ORDER BY name COLLATE NOCASE")
        return [row[0] for row in rows]

    def close(self) -> None:
        self.connection.close()