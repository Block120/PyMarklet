---
sidebar_position: 7
title: FAQ
description: Short answers to common PyMarklet questions.
---

# Frequently asked questions

## Does the bookmarklet use my local Python installation?

No. The bookmarklet downloads Pyodide, a WebAssembly build of CPython, and runs
your script in the browser. Your local Python is only used by the `pymarklet`
generator.

## Can I install packages with pip?

Not directly. Pyodide uses `micropip`, and PyMarklet installs packages
automatically from imports and the `# PKGS:` manifest. There is no shell, and
packages must have Pyodide-compatible wheels. See
[Dependencies](./guides/dependencies.md).

## Why is my bookmarklet URL so long?

The URL contains the entire JavaScript loader plus your source. It is already
several thousand characters before you add a script. Keep scripts small, and
fetch large data at runtime instead of embedding it.

## Why does nothing happen when I activate the bookmark?

Common causes:

- The page's Content Security Policy blocks injected scripts or remote fetches.
- The bookmark URL was truncated by the browser or a sync service.
- The URL was not saved as a complete `javascript:` URL.

Try the bookmarklet on a simple page, then check the panel on a page you trust.

## Does it work offline?

No. Pyodide is fetched from jsDelivr, and additional packages may be fetched from
PyPI-compatible hosts.

## Can my script read files from my computer?

No. Pyodide runs in the browser sandbox and cannot read your local filesystem.
You can fetch resources over HTTP with `pyodide.http.pyfetch` if the page's
network policy allows it.

## Can I use `tkinter` or other desktop GUI toolkits?

No. Only Pyodide-compatible libraries work. For graphics, use the panel canvas
with Pygame or a canvas-aware library; see
[Graphical apps](./guides/graphical-apps.md).

## Can I share a bookmarklet?

Yes, but remember that the Python source is embedded in the URL and can be read
by anyone who has it. Never embed secrets, credentials, or private data, and only
share bookmarklets whose behavior you are comfortable exposing.

## How do I update a bookmarklet?

Upgrade `pymarklet`, regenerate the URL from the source, and replace the
bookmark's URL. Bookmarklets do not update themselves.

## Which Pyodide version is used?

The current release pins Pyodide `0.27.5`. The version is exposed as
`pymarklet.generator.PYODIDE_VERSION`.

## Next steps

- [Limitations](./limitations.md)
- [Security and privacy](./security.md)
