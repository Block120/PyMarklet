"""Command-line interface for PyMarklet."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from .generator import generate_bookmarklet


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate a Pyodide-powered browser bookmarklet from a Python script.",
    )
    parser.add_argument("python_file", type=Path, help="UTF-8 Python source file to embed")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("bookmarklet.js"),
        help="destination for the bookmarklet URL (default: bookmarklet.js)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the PyMarklet CLI and return a process exit status."""
    args = build_parser().parse_args(argv)
    return 0 if generate_bookmarklet(args.python_file, args.output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
