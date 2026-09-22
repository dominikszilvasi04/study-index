from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    id: int
    name: str


@dataclass(frozen=True)
class LinkedFolder:
    id: int
    module_id: int
    path: str


@dataclass(frozen=True)
class FileMetadata:
    full_path: str
    file_name: str
    extension: str
    size_bytes: int
    modified_timestamp: float
