import sqlite3
from pathlib import Path
from study_index.modules.models import LinkedFolder, Module


class ModuleDatabase:
    def __init__(self, database_path: Path) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(database_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("CREATE TABLE IF NOT EXISTS modules (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS linked_folders (id INTEGER PRIMARY KEY, module_id INTEGER NOT NULL, path TEXT NOT NULL, UNIQUE(module_id, path), FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE CASCADE)")

    def add_module(self, name: str) -> Module | None:
        insert_result = self.connection.execute("INSERT OR IGNORE INTO modules (name) VALUES (?)", (name,))
        self.connection.commit()
        if insert_result.rowcount == 0:
            return None
        module_id = insert_result.lastrowid
        if module_id is None:
            raise RuntimeError("SQLite did not return an ID for the new module")
        return Module(module_id, name)

    def get_modules(self) -> list[Module]:
        rows = self.connection.execute("SELECT id, name FROM modules ORDER BY name COLLATE NOCASE")
        return [Module(row[0], row[1]) for row in rows]

    def rename_module(self, module_id: int, name: str) -> bool:
        update_result = self.connection.execute("UPDATE OR IGNORE modules SET name = ? WHERE id = ?", (name, module_id))
        self.connection.commit()
        return update_result.rowcount == 1

    def delete_module(self, module_id: int) -> bool:
        delete_result = self.connection.execute("DELETE FROM modules WHERE id = ?", (module_id,))
        self.connection.commit()
        return delete_result.rowcount == 1

    def add_linked_folder(self, module_id: int, path: str) -> LinkedFolder | None:
        insert_result = self.connection.execute("INSERT OR IGNORE INTO linked_folders (module_id, path) VALUES (?, ?)", (module_id, path))
        self.connection.commit()
        if insert_result.rowcount == 0:
            return None
        linked_folder_id = insert_result.lastrowid
        if linked_folder_id is None:
            raise RuntimeError("SQLite did not return an ID for the new linked folder")
        return LinkedFolder(linked_folder_id, module_id, path)

    def get_linked_folders(self, module_id: int) -> list[LinkedFolder]:
        rows = self.connection.execute("SELECT id, module_id, path FROM linked_folders WHERE module_id = ? ORDER BY path COLLATE NOCASE", (module_id,))
        return [LinkedFolder(row[0], row[1], row[2]) for row in rows]

    def remove_linked_folder(self, linked_folder_id: int) -> bool:
        delete_result = self.connection.execute("DELETE FROM linked_folders WHERE id = ?", (linked_folder_id,))
        self.connection.commit()
        return delete_result.rowcount == 1

    def close(self) -> None:
        self.connection.close()
