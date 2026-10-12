from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from urllib.parse import unquote

from pymarklet.generator import (
    PYODIDE_BASE_URL,
    PYODIDE_SCRIPT_URL,
    build_bookmarklet,
    declared_pypi_packages,
    generate_bookmarklet,
    imported_package_modules,
)


class DeclaredPyPiPackagesTests(unittest.TestCase):
    def test_reads_deduplicated_first_line_manifest(self) -> None:
        source = "# PKGS: python-dateutil, cowsay, python-dateutil, , emoji\nimport emoji\n"
        self.assertEqual(declared_pypi_packages(source), ["python-dateutil", "cowsay", "emoji"])

    def test_accepts_case_and_bom(self) -> None:
        self.assertEqual(declared_pypi_packages("\ufeff # pkgs: package>=1\n"), ["package>=1"])

    def test_ignores_manifest_not_on_first_line(self) -> None:
        self.assertEqual(declared_pypi_packages("\n# PKGS: cowsay\n"), [])


class ImportedPackageModulesTests(unittest.TestCase):
    def test_extracts_top_level_absolute_imports_in_order(self) -> None:
        source = """import alpha.beta
import gamma as g, alpha
from delta.epsilon import item
from .local import helper
"""
        self.assertEqual(imported_package_modules(source), ["alpha", "gamma", "delta"])

    def test_returns_empty_list_for_invalid_python(self) -> None:
        self.assertEqual(imported_package_modules("def invalid(:\n"), [])


class BookmarkletTests(unittest.TestCase):
    def test_embeds_escaped_source_and_runtime_urls(self) -> None:
        source = '# PKGS: package-name>=1\nprint("snowman: ☃ // remains source")\n'
        bookmarklet = build_bookmarklet(source)
        payload = unquote(bookmarklet.removeprefix("javascript:"))

        self.assertTrue(bookmarklet.startswith("javascript:"))
        self.assertNotIn("\n", bookmarklet)
        self.assertIn(f"const pyCode = {json.dumps(source)};", payload)
        self.assertIn('const declaredPackages = ["package-name>=1"];', payload)
        self.assertIn("const packageModules = [];", payload)
        self.assertIn(PYODIDE_BASE_URL, payload)
        self.assertIn(PYODIDE_SCRIPT_URL, payload)
        self.assertNotIn("__DATA_SPLICING_PLACEHOLDER__", payload)

    def test_writes_bookmarklet_to_requested_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.py"
            output = root / "nested" / "bookmarklet.txt"
            source.write_text("print('hello')\n", encoding="utf-8")
            output.parent.mkdir()

            with redirect_stdout(io.StringIO()) as stdout:
                success = generate_bookmarklet(source, output)

            self.assertTrue(success)
            self.assertTrue(output.read_text(encoding="utf-8").startswith("javascript:"))
            self.assertIn("Bookmarklet written to", stdout.getvalue())

    def test_reports_a_missing_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bookmarklet.txt"
            with redirect_stdout(io.StringIO()) as stdout:
                success = generate_bookmarklet(Path(directory) / "missing.py", output)

            self.assertFalse(success)
            self.assertFalse(output.exists())
            self.assertIn("Error reading", stdout.getvalue())
