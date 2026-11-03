---
sidebar_position: 1
title: Installation
description: Install the PyMarklet generator and check browser requirements.
---

# Installation

PyMarklet is a pure-Python package with no runtime dependencies. Installing it
only gives you the generator; the bookmarklet itself runs entirely in the
browser.

## Install the generator

```sh
python -m pip install pymarklet
```

Or, with [uv](https://docs.astral.sh/uv/):

```sh
uv add pymarklet
```

To try it without adding it to a project:

```sh
uvx pymarklet --help
```

## Verify the install

```sh
pymarklet --help
```

You should see the command synopsis:

```text
usage: pymarklet [-h] [-o OUTPUT] python_file
```

If the command is not found, make sure the environment where `pip` installed the
package is on your `PATH`. With uv, run `uv run pymarklet --help` inside the
project instead.

## Generator requirements

- **Python 3.11 or later.** This is the version that runs the CLI, not the
  version that runs your script in the browser.
- Any operating system supported by Python.

## Browser requirements

The generated bookmarklet targets modern browsers:

- WebAssembly and `async`/`await` support (current Chrome, Edge, Firefox, and
  Safari releases).
- A page where injected scripts are allowed. A strict Content Security Policy
  (CSP) can block the loader, package downloads, or browser APIs.
- Network access to `cdn.jsdelivr.net`. Additional packages may require access to
  PyPI-compatible hosts.
- The ability to store a long bookmark URL. Some browsers or sync services
  truncate very long bookmarks.

## Updating

Upgrade the generator with your package manager:

```sh
python -m pip install --upgrade pymarklet
```

Bookmarklets do not update themselves. Regenerate a bookmarklet after upgrading
to pick up generator fixes and the Pyodide version pinned by the new release.

## Next steps

- [Generate your first bookmarklet](./quickstart.md)
