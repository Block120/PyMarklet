---
sidebar_position: 3
title: Writing scripts
description: How PyMarklet scripts produce output, use async code, and stay small.
---

# Writing scripts

A PyMarklet script is ordinary Python source. The generator preserves it
verbatim and embeds it in the bookmarklet; there are no PyMarklet-specific
imports or decorators.

## Output

`print()` writes to the panel's output area, and uncaught exceptions appear
there as a traceback. Standard error is routed to the same place, so
`traceback.print_exc()` and warnings are visible too.

```python
import sys

print("standard output")
print("standard error", file=sys.stderr)
```

There is no terminal: the panel is append-only output, so prompt-driven
programs that expect an interactive console will not feel native.

## Async code

The bookmarklet calls `runPythonAsync`, which supports top-level `await`:

```python
import asyncio

await asyncio.sleep(0.1)
print("awaited")
```

To let the script return immediately while work continues in the background,
schedule a task:

```python
import asyncio


async def main() -> None:
    for _ in range(3):
        print("tick")
        await asyncio.sleep(1)


asyncio.create_task(main())
```

The integration example uses this pattern so the panel becomes usable before
the animation loop starts.

## State and lifetime

- The panel is created once per activation. If a panel with the same ID already
  exists, the loader returns without starting a second runtime.
- Closing the panel removes its UI but does not forcibly cancel Python work that
  is already scheduled in the page.
- Reloading the page discards the Python runtime and the panel.

## Keep scripts small

The JavaScript loader is already several thousand characters long, and the URL
grows roughly with the size of your source. Browsers and bookmark sync services
impose practical limits, so:

- Keep scripts short and focused.
- Store large data outside the script when possible, and fetch it at runtime
  with `pyodide.http.pyfetch`.
- Regenerate the bookmarklet after editing the source.

## Never embed secrets

The Python source is embedded in the bookmarklet URL and can be extracted by
anyone who has the URL. Never include API keys, tokens, credentials, private
endpoints, or sensitive data. See [Security and privacy](../security.md).

## Next steps

- [Handle dependencies](../guides/dependencies.md)
- [Use the canvas](../guides/graphical-apps.md)
