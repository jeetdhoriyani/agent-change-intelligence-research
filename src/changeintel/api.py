from __future__ import annotations

from pathlib import Path

from .git_diff import get_diff, parse_diff, read_at_ref, repository_root
from .models import AnalysisResult
from .symbols import changed_symbols_for_file


def analyze_repository(repo: str | Path = ".", base_ref: str = "HEAD~1") -> AnalysisResult:
    root = repository_root(Path(repo).resolve())
    changes = parse_diff(get_diff(root, base_ref))
    symbols = []
    warnings: list[str] = []

    for change in changes:
        old_source = (
            read_at_ref(root, base_ref, change.old_path)
            if change.old_path is not None
            else None
        )
        new_source = None
        if change.new_path is not None:
            path = root / change.new_path
            if path.exists():
                new_source = path.read_text(encoding="utf-8")
        file_symbols, file_warnings = changed_symbols_for_file(
            change, old_source, new_source
        )
        symbols.extend(file_symbols)
        warnings.extend(file_warnings)

    return AnalysisResult(
        schema_version="0.1",
        repository=str(root),
        base_ref=base_ref,
        files=changes,
        symbols=symbols,
        warnings=warnings,
    )
