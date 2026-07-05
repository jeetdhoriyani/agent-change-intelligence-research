from changeintel.models import FileChange, LineRange
from changeintel.symbols import changed_symbols_for_file, extract_definitions


def test_extract_nested_qualified_names() -> None:
    source = """class Cache:\n    def get(self):\n        return 1\n\nasync def load():\n    return 2\n"""
    definitions = extract_definitions(source)
    assert [(item.qualified_name, item.kind) for item in definitions] == [
        ("Cache", "class"),
        ("Cache.get", "function"),
        ("load", "async_function"),
    ]


def test_detect_added_modified_and_deleted_symbols() -> None:
    old = """def keep():\n    return 1\n\ndef remove():\n    return 2\n"""
    new = """def keep():\n    return 3\n\ndef added():\n    return 4\n"""
    change = FileChange(
        old_path="module.py",
        new_path="module.py",
        change_type="modified",
        old_ranges=[LineRange(1, 5)],
        new_ranges=[LineRange(1, 5)],
    )
    symbols, warnings = changed_symbols_for_file(change, old, new)
    assert warnings == []
    assert {(item.qualified_name, item.change_type) for item in symbols} == {
        ("keep", "modified"),
        ("remove", "deleted"),
        ("added", "added"),
    }
