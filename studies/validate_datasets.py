from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PROJECT_COLUMNS = {
    "project_name",
    "category",
    "repository_url",
    "status",
    "source_urls",
    "retrieved_at",
}


def validate_csv(path: Path, required: set[str]) -> list[str]:
    errors: list[str] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = required - headers
        if missing:
            errors.append(f"{path}: missing columns {sorted(missing)}")
            return errors
        for line_number, row in enumerate(reader, start=2):
            for column in required:
                if not (row.get(column) or "").strip():
                    errors.append(f"{path}:{line_number}: empty required field {column}")
    return errors


def main() -> int:
    errors = validate_csv(
        ROOT / "landscape" / "projects.csv", REQUIRED_PROJECT_COLUMNS
    )
    if errors:
        print("Dataset validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Dataset validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
