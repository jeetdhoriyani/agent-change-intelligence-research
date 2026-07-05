from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .models import FileChange, LineRange

_DIFF_HEADER = re.compile(r"^diff --git a/(.+) b/(.+)$")
_HUNK_HEADER = re.compile(
    r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"
)


class GitError(RuntimeError):
    pass


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if check and process.returncode != 0:
        message = process.stderr.strip() or process.stdout.strip()
        raise GitError(message or f"git {' '.join(args)} failed")
    return process.stdout


def repository_root(repo: Path) -> Path:
    return Path(run_git(repo, "rev-parse", "--show-toplevel").strip()).resolve()


def get_diff(repo: Path, base_ref: str) -> str:
    return run_git(
        repo,
        "diff",
        "--unified=0",
        "--find-renames",
        "--no-color",
        base_ref,
        "--",
        "*.py",
    )


def _range(start: int, count_text: str | None) -> LineRange | None:
    count = int(count_text) if count_text is not None else 1
    if count == 0:
        return None
    return LineRange(start=start, end=start + count - 1)


def parse_diff(diff_text: str) -> list[FileChange]:
    changes: list[FileChange] = []
    current: dict[str, object] | None = None

    def finish() -> None:
        nonlocal current
        if current is None:
            return
        old_path = current["old_path"]
        new_path = current["new_path"]
        status = current.get("status")
        if status == "added":
            change_type = "added"
            old_path = None
        elif status == "deleted":
            change_type = "deleted"
            new_path = None
        elif status == "renamed" or old_path != new_path:
            change_type = "renamed"
        else:
            change_type = "modified"
        changes.append(
            FileChange(
                old_path=old_path if isinstance(old_path, str) else None,
                new_path=new_path if isinstance(new_path, str) else None,
                change_type=change_type,
                old_ranges=list(current["old_ranges"]),
                new_ranges=list(current["new_ranges"]),
            )
        )
        current = None

    for line in diff_text.splitlines():
        header = _DIFF_HEADER.match(line)
        if header:
            finish()
            current = {
                "old_path": header.group(1),
                "new_path": header.group(2),
                "old_ranges": [],
                "new_ranges": [],
            }
            continue
        if current is None:
            continue
        if line.startswith("new file mode"):
            current["status"] = "added"
        elif line.startswith("deleted file mode"):
            current["status"] = "deleted"
        elif line.startswith("rename from "):
            current["old_path"] = line.removeprefix("rename from ")
            current["status"] = "renamed"
        elif line.startswith("rename to "):
            current["new_path"] = line.removeprefix("rename to ")
            current["status"] = "renamed"
        else:
            hunk = _HUNK_HEADER.match(line)
            if hunk:
                old_range = _range(int(hunk.group(1)), hunk.group(2))
                new_range = _range(int(hunk.group(3)), hunk.group(4))
                if old_range is not None:
                    current["old_ranges"].append(old_range)
                if new_range is not None:
                    current["new_ranges"].append(new_range)
    finish()
    return changes


def read_at_ref(repo: Path, ref: str, path: str) -> str | None:
    process = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{path}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        return None
    return process.stdout
