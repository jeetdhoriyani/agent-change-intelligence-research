from __future__ import annotations

import argparse
import json
import sys

from .api import analyze_repository
from .git_diff import GitError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="changeintel",
        description="Analyze Python symbols changed since a Git reference.",
    )
    parser.add_argument("--repo", default=".", help="Path inside the Git repository")
    parser.add_argument("--base", default="HEAD~1", help="Git reference to compare")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="text",
        dest="output_format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = analyze_repository(args.repo, args.base)
    except (GitError, OSError) as exc:
        if args.output_format == "json":
            print(
                json.dumps(
                    {
                        "error": {
                            "code": "ANALYSIS_FAILED",
                            "message": str(exc),
                            "recoverable": True,
                        }
                    },
                    indent=2,
                )
            )
        else:
            print(f"changeintel: {exc}", file=sys.stderr)
        return 2

    if args.output_format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Repository: {result.repository}")
        print(f"Base: {result.base_ref}")
        print(f"Changed Python files: {len(result.files)}")
        print(f"Changed symbols: {len(result.symbols)}")
        for symbol in result.symbols:
            print(
                f"- {symbol.change_type:8} {symbol.kind:14} "
                f"{symbol.path}:{symbol.start_line} {symbol.qualified_name}"
            )
        for warning in result.warnings:
            print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
