#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "click",
# ]
# ///

import json
from pathlib import Path

import click

TYPE_LABELS = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactoring",
    "doc": "Documentation",
    "test": "Tests",
    "ci": "CI",
    "build": "Build",
    "chore": "Chores",
    "style": "Style",
}


@click.command()
@click.option("--changelog-file", required=True, type=click.Path(exists=True, path_type=Path))
def main(changelog_file: Path) -> None:
    """Convert changelog JSON to GitHub release markdown."""
    data = json.loads(changelog_file.read_text())

    lines: list[str] = []
    for typ, entries in data["new_changes"].items():
        lines.append(f"### {TYPE_LABELS.get(typ, typ.title())}")
        for e in entries:
            scope = f"**{', '.join(e['scopes'])}**: " if e["scopes"] else ""
            lines.append(f"- {scope}{e['subject']} ({e['sha'][:7]})")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
