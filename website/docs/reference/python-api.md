---
sidebar_position: 2
title: Python API
description: Programmatic generation and import inspection with pymarklet.
---

# Python API

PyMarklet exposes a small library alongside the CLI. The public names are
re-exported from the package root:

```python
from pymarklet import (
    build_bookmarklet,
    declared_pypi_packages,
    imported_package_modules,
)
```

`generate_bookmarklet`, the constants, and the internal helpers live in
`pymarklet.generator`.

## `build_bookmarklet`

```python
def build_bookmarklet(python_code: str) -> str
```

Build a bookmarklet URL from Python source.

- **`python_code`** — the exact source to embed.
- **Returns** — a string beginning with `javascript:` followed by the
  percent-encoded loader.
- **Notes** — the source is embedded with `json.dumps`, so quotes and newlines
  are encoded safely. Syntax is not validated; Pyodide reports syntax errors when
  the bookmarklet runs.

```python
from pathlib import Path

from pymarklet import build_bookmarklet

source = Path("hello.py").read_text(encoding="utf-8")
url = build_bookmarklet(source)
Path("hello-bookmarklet.txt").write_text(url, encoding="utf-8")
```

## `generate_bookmarklet`

```python
def generate_bookmarklet(python_file_path: Path, output_path: Path) -> bool
```

Read a UTF-8 source file, build a bookmarklet, and write it to
`output_path`.

- **Returns** — `True` on success, `False` on a read or write failure.
- **Side effects** — prints a success message, or `Error reading ...` /
  `Error writing ...` on failure.
- **Notes** — the output directory must already exist.

This is the function used by the CLI.

```python
from pathlib import Path

from pymarklet.generator import generate_bookmarklet

ok = generate_bookmarklet(Path("hello.py"), Path("hello-bookmarklet.txt"))
```

## `declared_pypi_packages`

```python
def declared_pypi_packages(python_code: str) -> list[str]
```

Extract the first-line `# PKGS:` manifest.

- **Returns** — PyPI requirement strings in first-seen order, with blanks
  removed and duplicates dropped. Returns `[]` when no valid first-line manifest
  exists.
- **Notes** — leading whitespace and a UTF-8 BOM are tolerated. Matching is
  case-insensitive, so `# pkgs:` works.

```python
>>> from pymarklet import declared_pypi_packages
>>> declared_pypi_packages("# PKGS: python-dateutil, cowsay, python-dateutil\n")
['python-dateutil', 'cowsay']
```

## `imported_package_modules`

```python
def imported_package_modules(python_code: str) -> list[str]
```

Return the top-level absolute modules imported by the source.

- **Returns** — unique top-level module names in first-seen order. Relative
  imports (`from . import x`) and dynamic imports are not included.
- **Notes** — if the source cannot be parsed, returns `[]` and leaves the
  original syntax error for Pyodide to report.

```python
>>> from pymarklet import imported_package_modules
>>> imported_package_modules("import numpy as np\nfrom dateutil import parser\n")
['numpy', 'dateutil']
```

## Constants

Available from `pymarklet.generator`:

| Name | Value |
| --- | --- |
| `PYODIDE_VERSION` | `"0.27.5"` |
| `PYODIDE_BASE_URL` | `"https://cdn.jsdelivr.net/pyodide/v0.27.5/full/"` |
| `PYODIDE_SCRIPT_URL` | `"https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js"` |

The package version is available as `pymarklet.__version__`.

## Next steps

- [CLI reference](./cli.md)
- [Understand the generated runtime](./runtime.md)
