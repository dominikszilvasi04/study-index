from pathlib import Path

import pytest

import study_index.modules.module_database as module_database_module
from study_index.modules.models import LinkedFolder, Module
from study_index.modules.module_database import ModuleDatabase


def test_module_crud(tmp_path: Path) -> None:
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    module = module_database.add_module("Mathematics")
    assert module is not None
    assert module_database.add_module("Mathematics") is None
    assert not module_database.rename_module(999, "Missing")
    assert module_database.rename_module(module.id, "Physics")
    assert module_database.get_modules() == [Module(module.id, "Physics")]
    assert not module_database.delete_module(999)
    assert module_database.delete_module(module.id)
    assert module_database.get_modules() == []
    module_database.close()


def test_module_folders(tmp_path: Path) -> None:
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    module = module_database.add_module("Mathematics")
    linked_folder = module_database.add_linked_folder(module.id, "C:/College/Mathematics")
    assert linked_folder is not None
    assert module_database.add_linked_folder(module.id, linked_folder.path) is None
    assert module_database.get_linked_folders(module.id) == [LinkedFolder(linked_folder.id, module.id, linked_folder.path)]
    assert not module_database.remove_linked_folder(999)
    assert module_database.remove_linked_folder(linked_folder.id)
    assert module_database.get_linked_folders(module.id) == []
    module_database.close()


def test_modules_and_folders_are_sorted_case_insensitively(tmp_path: Path) -> None:
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    zebra_module = module_database.add_module("zebra")
    alpha_module = module_database.add_module("Alpha")
    assert zebra_module is not None
    assert alpha_module is not None
    second_folder = module_database.add_linked_folder(alpha_module.id,
                                                      "C:/zebra")
    first_folder = module_database.add_linked_folder(alpha_module.id,
                                                     "C:/Alpha")
    assert module_database.get_modules() == [alpha_module, zebra_module]
    assert module_database.get_linked_folders(alpha_module.id) == [
        first_folder, second_folder
    ]
    module_database.close()


def test_deleting_module_deletes_its_linked_folders(tmp_path: Path) -> None:
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    module = module_database.add_module("Mathematics")
    assert module is not None
    module_database.add_linked_folder(module.id, "C:/College")
    assert module_database.delete_module(module.id)
    assert module_database.get_linked_folders(module.id) == []
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


def test_missing_sqlite_insert_ids_are_reported(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    connection = ConnectionWithoutInsertIds()
    monkeypatch.setattr(module_database_module.sqlite3,
                        "connect",
                        lambda database_path: connection)
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    with pytest.raises(RuntimeError, match="ID for the new module"):
        module_database.add_module("Mathematics")
    with pytest.raises(RuntimeError, match="ID for the new linked folder"):
        module_database.add_linked_folder(1, "C:/College")
