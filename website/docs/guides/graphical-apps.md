---
sidebar_position: 2
title: Graphical apps and the canvas
description: Draw to the bookmarklet panel with Pyodide-compatible graphics libraries.
---

# Graphical apps and the canvas

The panel includes a `<canvas>` element in addition to the output area. Before
running your script, the loader calls `pyodide.canvas.setCanvas2D(canvas)`, so
libraries that use Pyodide's canvas bridge can draw directly into the panel.

## What works

- **Pygame.** Pyodide ships a Pygame build that renders to the Pyodide canvas.
- **Other canvas-aware libraries.** Any library that uses Pyodide's canvas APIs
  can target the same element.
- **`print()` alongside graphics.** Status and text output still appear below
  the canvas.

The canvas is sized by the library; the panel constrains it to `max-width: 100%`
and `max-height: 70%` of the panel so it does not overflow.

## Keyboard input

The canvas is focusable. Click it before sending keyboard input:

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((320, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((15, 18, 26))
    pygame.display.flip()
```

The loader also focuses the canvas on `pointerdown`, so a simple click is enough
to give it keyboard focus.

## An async animation loop

Long-running loops must yield to the browser event loop, or the page will stop
responding. Use `asyncio.sleep` instead of `pygame.time.wait` or a busy loop:

```python
import asyncio

import pygame


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((320, 200))
    position = [160, 100]

    for frame in range(180):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("stopped with Escape")
                return

        position[0] = (position[0] + 3) % 320
        screen.fill((15, 18, 26))
        pygame.draw.circle(screen, (80, 200, 255), position, 8)
        pygame.display.flip()

        await asyncio.sleep(1 / 60)


asyncio.create_task(main())
```

Scheduling the coroutine with `asyncio.create_task` lets the bookmarklet finish
starting Python while the animation runs in the background.

:::caution[Avoid pygame.quit() in an active callback]

Pyodide's Pygame backend is attached to the browser event loop. Tearing it down
while a Pygame callback is active can leave the runtime in a bad state. The
integration example deliberately stops its loop without calling `pygame.quit()`.

:::

## Closing the panel

Clicking **×** removes the panel but does not cancel Python work already
scheduled in the page. If your script must stop cleanly, use a flag or an early
exit in the loop rather than relying on the close button.

## Next steps

- [Run the integration example](./examples.md)
- [Review limitations](../limitations.md)
