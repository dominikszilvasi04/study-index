import sqlite3
from pathlib import Path

from study_index.modules.modules_model import Module


class ModuleRepository:
    def __init__(self, database_path: Path):
        self.connection = sqlite3.connect(database_path)
        self.connection.execute("CREATE TABLE IF NOT EXISTS modules (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")

    def add(self, name: str) -> Module | None:
        cursor = self.connection.execute("INSERT OR IGNORE INTO modules (name) VALUES (?)", (name,))
        self.connection.commit()
        if cursor.rowcount == 0:
            return None
        return Module(cursor.lastrowid, name)

    def all(self) -> list[Module]:
        rows = self.connection.execute("SELECT id, name FROM modules ORDER BY name COLLATE NOCASE")
        return [Module(row[0], row[1]) for row in rows]

    def update(self, module_id: int, name: str) -> bool:
        cursor = self.connection.execute("UPDATE OR IGNORE modules SET name = ? WHERE id = ?", (name, module_id))
        self.connection.commit()
        return cursor.rowcount == 1

    def delete(self, module_id: int) -> bool:
        cursor = self.connection.execute("DELETE FROM modules WHERE id = ?", (module_id,))
        self.connection.commit()
        return cursor.rowcount == 1

    def close(self) -> None:
        self.connection.close()
