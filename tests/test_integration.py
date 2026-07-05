import json
import subprocess
from pathlib import Path

from changeintel.api import analyze_repository
from changeintel.cli import main


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def test_analyze_repository_and_json_cli(tmp_path: Path, capsys) -> None:
    git(tmp_path, "init")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "Test")
    module = tmp_path / "module.py"
    module.write_text("def value():\n    return 1\n", encoding="utf-8")
    git(tmp_path, "add", "module.py")
    git(tmp_path, "commit", "-m", "initial")
    module.write_text("def value():\n    return 2\n", encoding="utf-8")

    result = analyze_repository(tmp_path, "HEAD")
    assert len(result.files) == 1
    assert [(item.qualified_name, item.change_type) for item in result.symbols] == [
        ("value", "modified")
    ]

    assert main(["--repo", str(tmp_path), "--base", "HEAD", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == "0.1"
    assert payload["symbols"][0]["qualified_name"] == "value"
