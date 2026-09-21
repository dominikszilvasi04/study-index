from dataclasses import dataclass


@dataclass(frozen=True)
class Module:
    id: int
    name: str
