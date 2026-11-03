---
sidebar_position: 3
title: Examples
description: Run the bundled integration stress test and sandbox page.
---

# Examples

The repository includes a manual integration example under `examples/`. It
exercises dependency resolution, NumPy, Pyodide networking, and a bounded Pygame
animation.

## Integration stress test

`examples/integration_stress_test.py` covers:

- A first-line `# PKGS:` manifest with distribution names
  (`cowsay`, `more-itertools`, `python-dateutil`).
- A mismatched import name (`python-dateutil` imported as `dateutil`).
- Automatic fallback installation for `emoji`, which is not declared.
- A Pyodide-provided native package (`numpy`).
- A Pygame animation bound to the panel canvas.
- An HTTP request through `pyodide.http.pyfetch`.

Generate the bookmarklet:

```sh
pymarklet examples/integration_stress_test.py
```

By default the output is `bookmarklet.js` in the current directory.

## Sandbox page

`examples/sandbox.html` is a minimal page you can use as a target:

```sh
python -m http.server 8000
```

Open `http://localhost:8000/examples/sandbox.html` (or open the file directly in
your browser), then activate the generated bookmarklet on it.

The first run downloads Pyodide and several packages, so it can take a while.
The animation runs for 180 frames. Click the canvas and press **Escape** to stop
early.

## What to look for

| Output | Meaning |
| --- | --- |
| `cowsay` art | Declared distribution installed and imported. |
| `dateutil parsed:` | Distribution name differs from import name and still works. |
| `automatic fallback installed` | Undeclared `emoji` import was resolved by name. |
| `numpy matrix:` | A Pyodide-provided native package ran. |
| `network HTTP 200` | `pyfetch` reached the network. A different message means networking was unavailable. |
| `canvas: ...` | The Pygame loop is rendering to the panel canvas. |

## A smaller example

For a quick smoke test without third-party packages:

```python
import sys
import platform

print("Python", platform.python_version())
print("Platform", sys.platform)
```

Run `pymarklet smoke.py -o smoke.txt`, save the URL as a bookmark, and activate
it on any page.

## Next steps

- [Read the CLI reference](../reference/cli.md)
- [Understand the generated runtime](../reference/runtime.md)
