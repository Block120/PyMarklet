from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from pymarklet.cli import main


class CliTests(unittest.TestCase):
    def test_generates_to_default_output_in_current_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "script.py"
            source.write_text("print('hello')\n", encoding="utf-8")

            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                self.assertEqual(main([str(source)]), 0)
            finally:
                os.chdir(previous_directory)

            self.assertTrue((root / "bookmarklet.js").exists())

    def test_returns_failure_for_missing_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(main([str(root / "missing.py"), "-o", str(root / "output.txt")]), 1)
