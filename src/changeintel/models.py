from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

ChangeType = Literal["added", "modified", "deleted", "renamed"]
SymbolKind = Literal["function", "async_function", "class"]


@dataclass(frozen=True)
class LineRange:
    start: int
    end: int


@dataclass(frozen=True)
class FileChange:
    old_path: str | None
    new_path: str | None
    change_type: ChangeType
    old_ranges: list[LineRange] = field(default_factory=list)
    new_ranges: list[LineRange] = field(default_factory=list)


@dataclass(frozen=True)
class ChangedSymbol:
    path: str
    qualified_name: str
    kind: SymbolKind
    change_type: Literal["added", "modified", "deleted"]
    start_line: int
    end_line: int


@dataclass(frozen=True)
class AnalysisResult:
    schema_version: str
    repository: str
    base_ref: str
    files: list[FileChange]
    symbols: list[ChangedSymbol]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
