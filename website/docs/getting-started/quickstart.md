---
sidebar_position: 2
title: Quick start
description: Generate and run your first PyMarklet bookmarklet in five steps.
---

# Quick start

This walkthrough takes a one-line Python script and turns it into a working
browser bookmarklet.

## 1. Write a Python script

Create a file named `hello.py`:

```python
# hello.py
print("Hello from Python in your browser!")
```

## 2. Generate the bookmarklet

```sh
pymarklet hello.py -o hello-bookmarklet.txt
```

The command writes a single `javascript:` URL to `hello-bookmarklet.txt` and
prints the URL length. That length matters — see
[Bookmark URL length](./writing-scripts.md#keep-scripts-small).

## 3. Copy the URL

Open `hello-bookmarklet.txt` and copy its **complete** contents. Do not add line
breaks or wrap the text; the whole file is one URL.

## 4. Create a bookmark

In your browser:

1. Open the bookmark manager.
2. Create a new bookmark named **PyMarklet: hello**.
3. Paste the copied `javascript:` URL into the bookmark's **URL** (or
   **location**) field.
4. Save it.

:::note[Pasting into the address bar]

Many browsers strip or block `javascript:` URLs typed or pasted into the address
bar. Paste the URL into a bookmark's URL field instead.

:::

## 5. Run it on a page

Visit any page (for example, a search engine or a blank tab) and activate the
bookmark. A panel appears in the upper-right corner:

- The header shows the current status, such as `Loading Pyodide...` or
  `Execution finished.`
- The dark area below the canvas displays `print()` output and errors.
- Drag the header to move the panel.
- Click **×** to remove the panel.
- If your script uses a canvas, click the canvas before sending keyboard input.

The first run downloads Pyodide and can take several seconds. Later runs may be
faster if your browser has cached the runtime.

## Try something interactive

```python
import asyncio
import math


async def main() -> None:
    for step in range(6):
        print(f"step {step}: {math.sin(step):.3f}")
        await asyncio.sleep(0.5)


await main()
```

PyMarklet runs source with `runPythonAsync`, so top-level `await` is supported.
You can also start a background task with `asyncio.create_task(main())`, as the
[integration example](../guides/examples.md) does.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| Nothing happens when the bookmark is activated | The page's CSP blocks injected scripts, or the bookmark URL was truncated. |
| Status stays on `Loading Pyodide...` | jsDelivr is blocked by the network, an ad blocker, or a proxy. |
| `Could not load Pyodide (possibly blocked by CSP).` | The runtime script failed to load. Try another page or network. |
| A package fails to install | No WebAssembly-compatible wheel exists, or PyPI access is blocked. |
| The bookmark disappeared or became invalid | The browser or sync service rejected the long URL. Shorten the script. |

## Next steps

- [Write scripts that work well in a bookmarklet](./writing-scripts.md)
- [Handle dependencies](../guides/dependencies.md)
- [Draw with Pygame](../guides/graphical-apps.md)
