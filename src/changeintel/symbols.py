from __future__ import annotations

import ast
from dataclasses import dataclass

from .models import ChangedSymbol, FileChange, LineRange, SymbolKind


@dataclass(frozen=True)
class SymbolDefinition:
    qualified_name: str
    kind: SymbolKind
    start_line: int
    end_line: int


class _DefinitionVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.scope: list[str] = []
        self.definitions: list[SymbolDefinition] = []

    def _record(self, node: ast.AST, name: str, kind: SymbolKind) -> None:
        qualified = ".".join([*self.scope, name])
        self.definitions.append(
            SymbolDefinition(
                qualified_name=qualified,
                kind=kind,
                start_line=getattr(node, "lineno"),
                end_line=getattr(node, "end_lineno", getattr(node, "lineno")),
            )
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record(node, node.name, "class")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record(node, node.name, "function")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record(node, node.name, "async_function")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()


def extract_definitions(source: str) -> list[SymbolDefinition]:
    tree = ast.parse(source)
    visitor = _DefinitionVisitor()
    visitor.visit(tree)
    return visitor.definitions


def _intersects(symbol: SymbolDefinition, ranges: list[LineRange]) -> bool:
    return any(
        symbol.start_line <= line_range.end
        and line_range.start <= symbol.end_line
        for line_range in ranges
    )


def changed_symbols_for_file(
    change: FileChange,
    old_source: str | None,
    new_source: str | None,
) -> tuple[list[ChangedSymbol], list[str]]:
    warnings: list[str] = []
    try:
        old_defs = extract_definitions(old_source) if old_source is not None else []
    except SyntaxError as exc:
        old_defs = []
        warnings.append(f"Could not parse old version of {change.old_path}: {exc}")
    try:
        new_defs = extract_definitions(new_source) if new_source is not None else []
    except SyntaxError as exc:
        new_defs = []
        warnings.append(f"Could not parse new version of {change.new_path}: {exc}")

    old_by_key = {(item.qualified_name, item.kind): item for item in old_defs}
    new_by_key = {(item.qualified_name, item.kind): item for item in new_defs}
    symbols: list[ChangedSymbol] = []

    for key, definition in new_by_key.items():
        old_definition = old_by_key.get(key)
        if old_definition is None:
            if change.change_type == "added" or _intersects(definition, change.new_ranges):
                symbols.append(
                    ChangedSymbol(
                        path=change.new_path or "",
                        qualified_name=definition.qualified_name,
                        kind=definition.kind,
                        change_type="added",
                        start_line=definition.start_line,
                        end_line=definition.end_line,
                    )
                )
        elif _intersects(definition, change.new_ranges) or _intersects(
            old_definition, change.old_ranges
        ):
            symbols.append(
                ChangedSymbol(
                    path=change.new_path or change.old_path or "",
                    qualified_name=definition.qualified_name,
                    kind=definition.kind,
                    change_type="modified",
                    start_line=definition.start_line,
                    end_line=definition.end_line,
                )
            )

    for key, definition in old_by_key.items():
        if key not in new_by_key and (
            change.change_type == "deleted" or _intersects(definition, change.old_ranges)
        ):
            symbols.append(
                ChangedSymbol(
                    path=change.old_path or "",
                    qualified_name=definition.qualified_name,
                    kind=definition.kind,
                    change_type="deleted",
                    start_line=definition.start_line,
                    end_line=definition.end_line,
                )
            )

    symbols.sort(key=lambda item: (item.path, item.start_line, item.qualified_name))
    return symbols, warnings
