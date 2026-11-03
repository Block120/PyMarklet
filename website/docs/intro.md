---
sidebar_position: 1
title: What is PyMarklet?
description: Turn a Python script into a bookmarklet that runs in the browser with Pyodide.
---

# What is PyMarklet?

PyMarklet generates a browser bookmarklet from a Python script. When you activate
the bookmarklet on a web page, it loads [Pyodide](https://pyodide.org/) — a
WebAssembly build of CPython — adds a draggable output panel, and runs your
embedded script inside the page.

You write Python, run one command, and get a `javascript:` URL you can save as a
browser bookmark:

```sh
pymarklet hello.py -o hello-bookmarklet.txt
```

The generated URL contains the full loader and your source code. It does not
depend on your local Python installation at runtime.

:::warning[Experimental]

PyMarklet executes code in the context of the page where the bookmarklet is
activated. Read [Security and privacy](./security.md) before sharing or running
a bookmarklet.

:::

## Why use it?

- **No extension or server.** A bookmarklet is just a bookmark with a
  `javascript:` URL.
- **Your Python, unmodified.** The generator embeds your source as-is; there is
  no transpilation step.
- **Automatic dependency resolution.** Imports are detected, Pyodide packages are
  loaded, and missing distributions can be installed from PyPI at runtime.
- **Graphics work too.** Pyodide's canvas is wired up, so libraries such as
  Pygame can draw into the panel.
- **One command.** The CLI has no configuration files and no runtime
  dependencies.

## How it fits together

1. **You run the generator.** `pymarklet script.py` reads your UTF-8 source,
   inspects its imports, and produces a percent-encoded `javascript:` URL.
2. **You save the URL as a bookmark.** The complete URL goes into the bookmark's
   URL/location field.
3. **You activate it on a page.** The loader injects a fixed-position panel,
   creates a canvas and an output area, and fetches Pyodide 0.27.5 from jsDelivr.
4. **Pyodide runs your script.** Recognized packages load through Pyodide's
   package loader; other distributions can be installed with `micropip`.
5. **Output appears in the panel.** `print()` and error text are appended to the
   output area, and graphical libraries can draw to the canvas.

## Requirements at a glance

| Component | Requirement |
| --- | --- |
| Generator | Python 3.11 or later |
| Browser | A modern browser with WebAssembly and `async`/`await` support |
| Network | Access to jsDelivr and, for extra packages, PyPI-compatible hosts |
| Script size | Small enough that the resulting URL fits your browser's limits |

## Next steps

- [Install PyMarklet](./getting-started/installation.md)
- [Generate your first bookmarklet](./getting-started/quickstart.md)
- [Understand dependency handling](./guides/dependencies.md)
- [Read the CLI reference](./reference/cli.md)
