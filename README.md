# PyMarklet

[![CI](https://github.com/Block120/PyMarklet/actions/workflows/ci.yml/badge.svg)](https://github.com/Block120/PyMarklet/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pymarklet.svg)](https://pypi.org/project/pymarklet/)
[![Python](https://img.shields.io/pypi/pyversions/pymarklet.svg)](https://pypi.org/project/pymarklet/)

Generate a browser bookmarklet that runs a Python script with [Pyodide](https://pyodide.org/). The generated bookmarklet adds a draggable output panel to the current page, loads Python in WebAssembly, and runs your embedded script in the browser.

> **Experimental:** PyMarklet executes code in the context of the web page where the bookmarklet is activated. Read the [Security and privacy](#security-and-privacy) section before sharing or running a bookmarklet.

## Installation

```sh
python -m pip install pymarklet
```

PyMarklet requires Python 3.11 or later to generate bookmarklets. The resulting bookmarklet runs Python in a supported modern browser; it does not use your local Python environment at runtime.

## Quick start

Create a Python script:

```python
# hello.py
print("Hello from Python in your browser!")
```

Generate a bookmarklet URL:

```sh
pymarklet hello.py -o hello-bookmarklet.txt
```

1. Open `hello-bookmarklet.txt` and copy its complete contents.
2. Create a browser bookmark named **PyMarklet: hello**.
3. Paste the copied `javascript:` URL into the bookmark's URL/location field.
4. Visit a webpage and activate the bookmark.

A panel appears in the upper-right corner with status and Python output. Drag its header to move it, click **×** to remove it, and click the canvas before sending keyboard input to graphical applications.

> Some browsers block pasting `javascript:` URLs into the address bar. Paste the URL into a bookmark's URL field instead.

## Command line

```text
pymarklet [-h] [-o OUTPUT] python_file
```

| Argument | Description |
| --- | --- |
| `python_file` | UTF-8 Python source file to embed. |
| `-o`, `--output` | Destination file for the bookmarklet URL. Defaults to `bookmarklet.js` in the current directory. |

The command returns a nonzero status if it cannot read the source or write the output file.

## Dependencies

PyMarklet determines dependencies in two stages when the bookmarklet runs:

1. It asks Pyodide to load packages it recognizes from normal `import` statements.
2. For missing imports, it attempts to install a package with the same name using `micropip`.

When a PyPI distribution name differs from its import name, declare it in a **first-line** manifest:

```python
# PKGS: python-dateutil, more-itertools
from dateutil import parser
from more_itertools import chunked

print(parser.isoparse("2026-10-10T12:34:56Z"))
print(list(chunked(range(6), 2)))
```

The manifest is comma-separated, case-insensitive (`# pkgs:` also works), trims duplicates, and accepts normal PyPI requirement specifiers such as `requests>=2.32`. Use it for every dependency whose import name is not its distribution name—for example, `scikit-learn` / `sklearn`.

## How it works

The generated URL embeds your source, creates a small page overlay, and loads **Pyodide 0.27.5** from jsDelivr. Standard output and errors appear in the overlay. The canvas is available to Pyodide-compatible graphical libraries such as Pygame.

The source in [`examples/integration_stress_test.py`](examples/integration_stress_test.py) and the page in [`examples/sandbox.html`](examples/sandbox.html) are a manual integration example:

```sh
pymarklet examples/integration_stress_test.py
```

Open `examples/sandbox.html` in a browser, then use the generated bookmarklet on that page.

## Limitations

- **Network access is required.** The browser fetches Pyodide from jsDelivr and may fetch packages from PyPI-compatible hosts.
- **Content Security Policy (CSP) can prevent execution.** Sites may block the injected Pyodide script, package downloads, or required browser APIs.
- **Only Pyodide-compatible packages work.** Native packages without compatible WebAssembly wheels cannot be installed.
- **Import detection is static and best-effort.** Dynamic imports and relative imports are not detected; use `# PKGS:` for dependencies that need explicit installation.
- **Bookmark URLs have practical length limits.** The loader is already several thousand characters long, and the URL grows with your script. Keep scripts small.
- Closing the overlay removes its UI but does not forcibly cancel Python work already scheduled in the page.

## Security and privacy

- A bookmarklet is executable code. Only run bookmarklets you trust.
- Your Python source is embedded in the bookmarklet URL. **Never include secrets, credentials, private endpoints, or sensitive data.** Anyone with the URL can extract the source.
- The bookmarklet executes with the permissions and network environment of the page where you activate it. Review site policies and do not use it on pages where injected code is inappropriate.
- Dependencies are downloaded and executed in the browser. Pin or constrain declared requirements where reproducibility matters.
- PyMarklet relies on jsDelivr to serve its pinned Pyodide runtime. Ad blockers, offline mode, proxies, or supply-chain policy may block it.

See [`SECURITY.md`](SECURITY.md) for vulnerability reporting.

## Development

```sh
uv sync
uv run python -m unittest discover -s tests -v
uv build
```

Contributions are welcome; see [`CONTRIBUTING.md`](CONTRIBUTING.md). This project is licensed under the [MIT License](LICENSE).

## Publishing checklist

Before the first public release, confirm the `pymarklet` name is available on PyPI and configure PyPI Trusted Publishing for this repository and the `pypi` GitHub environment.
