from pathlib import Path

from study_index.modules.models import LinkedFolder, Module
from study_index.modules.module_database import ModuleDatabase


def test_module_crud(tmp_path: Path) -> None:
    module_database = ModuleDatabase(tmp_path / "study_index.db")
    module = module_database.add_module("Mathematics")

    assert module is not None
    assert module_database.add_module("Mathematics") is None
    assert module_database.rename_module(module.id, "Physics")
    assert module_database.get_modules() == [Module(module.id, "Physics")]
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
    assert module_database.remove_linked_folder(linked_folder.id)
    assert module_database.get_linked_folders(module.id) == []

    module_database.close()
