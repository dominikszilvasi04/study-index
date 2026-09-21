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
