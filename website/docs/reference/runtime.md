---
sidebar_position: 3
title: Generated runtime
description: What the bookmarklet does after it is activated.
---

# Generated runtime

A bookmarklet is a single `javascript:` URL containing the entire loader. This
page describes what that loader does at runtime.

## URL structure

The generator produces:

```text
javascript:<percent-encoded-loader>
```

The loader embeds three JSON values directly into the script:

| Variable | Contents |
| --- | --- |
| `pyCode` | Your Python source, encoded with `json.dumps`. |
| `declaredPackages` | Distribution names from the first-line `# PKGS:` manifest. |
| `packageModules` | Top-level absolute imports found by static analysis. |

The runtime URLs for Pyodide are also substituted in:

- `https://cdn.jsdelivr.net/pyodide/v0.27.5/full/`
- `https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js`

## Activation sequence

1. Check for an existing panel with the ID `py-bookmarklet-container`. If it is
   present, return immediately.
2. Create the fixed-position panel: a draggable header, a close button, a
   focusable canvas, and a scrollable output area.
3. Load `pyodide.js` from jsDelivr unless `globalThis.loadPyodide` already
   exists.
4. Initialize Pyodide with `indexURL` pointing at the pinned version. `stdout`
   and `stderr` both append to the output area.
5. Connect the panel canvas with `pyodide.canvas.setCanvas2D`.
6. Run `loadPackagesFromImports(pyCode)`.
7. Install declared distributions with `micropip`.
8. For remaining detected imports that are not importable, install the matching
   PyPI name with `micropip`.
9. Execute the source with `runPythonAsync`.

Status messages appear in the header as each stage runs. Failures set the status
to `Python execution failed.` and write the error stack or message to the output
area.

## Panel behavior

- **Position** — fixed at the upper-right, `400px` by `500px`, with a very high
  `z-index`.
- **Dragging** — drag the header. The panel is clamped to the viewport, and the
  header uses pointer capture so the drag continues outside the header.
- **Close** — the **×** button removes the panel. It does not cancel work that
  Pyodide has already scheduled.
- **Canvas** — click it to focus before sending keyboard input. The loader also
  focuses it on `pointerdown`.
- **Output** — `print()` and standard error both append here. The area scrolls
  to the bottom after each write.

## Failure modes

| Failure | Result |
| --- | --- |
| Pyodide script cannot load | Status: `Could not load Pyodide (possibly blocked by CSP).` |
| A package cannot be installed | `Python execution failed.` with the install error. |
| The script raises an exception | `Python execution failed.` with the traceback. |
| The page blocks injected scripts | The bookmarklet may do nothing at all. |

## Next steps

- [Limitations](../limitations.md)
- [Security and privacy](../security.md)
