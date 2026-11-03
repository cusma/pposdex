"""
The CLI reference in the docs includes each command's `--help` output from
docs/cli/help. Regenerate it with `UPDATE_DOCS=1 uv run pytest test/test_docs.py`.
"""

import os
import sys
from pathlib import Path

import pytest

from pposdex.cli import build_parser

HELP_DIR = Path(__file__).parents[1] / "docs" / "cli" / "help"
COMMANDS = ["publish", "timeseries", "snapshot", "export", "health"]


@pytest.mark.skipif(
    sys.version_info < (3, 13),
    reason="argparse formats option help differently before 3.13",
)
@pytest.mark.parametrize("command", [None, *COMMANDS])
def test_cli_help_in_docs(
    command: str | None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("COLUMNS", "100")
    with pytest.raises(SystemExit):
        build_parser().parse_args([command, "--help"] if command else ["--help"])
    help_text = capsys.readouterr().out

    path = HELP_DIR / f"{command or 'pposdex'}.txt"
    if os.getenv("UPDATE_DOCS") == "1":
        path.write_text(help_text, encoding="utf8")
    assert help_text == path.read_text(encoding="utf8"), (
        "CLI help changed: run `UPDATE_DOCS=1 uv run pytest test/test_docs.py`"
    )
