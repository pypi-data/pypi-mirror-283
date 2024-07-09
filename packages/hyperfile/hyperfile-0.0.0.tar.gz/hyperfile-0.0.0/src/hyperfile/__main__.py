"""Support executing the CLI by doing `python -m hyperfile`."""
from __future__ import annotations

from hyperfile.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
