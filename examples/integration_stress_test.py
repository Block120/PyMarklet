# PKGS: cowsay, more-itertools, python-dateutil
"""PyMarklet generator integration stress test.

The first-line manifest deliberately uses PyPI distribution names. In
particular, ``python-dateutil`` is imported as ``dateutil``. The ``emoji``
import is omitted from the manifest to exercise the import-name fallback.
"""

import asyncio
from datetime import UTC

import cowsay  # pyright: ignore[reportMissingImports]
import emoji  # pyright: ignore[reportMissingImports]
import numpy as np  # pyright: ignore[reportMissingImports]
import pygame  # pyright: ignore[reportMissingImports]
from dateutil import parser as date_parser  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from more_itertools import chunked  # pyright: ignore[reportMissingImports]
from pyodide.http import pyfetch  # pyright: ignore[reportMissingImports]


async def fetch_status() -> str:
    """Verify that Pyodide's browser networking bridge is available."""
    try:
        response = await pyfetch("https://httpbin.org/get")
        return f"network HTTP {response.status}"
    except Exception as error:  # noqa: BLE001
        return f"network unavailable: {error}"


def dependency_report() -> None:
    """Exercise declared distributions, a mismatched import name, and fallback."""
    print(cowsay.get_output_string("cow", "PyMarklet dependencies loaded!"))

    parsed = date_parser.isoparse("2026-10-10T12:34:56Z")
    assert parsed.tzinfo is not None
    chunks = list(chunked(range(12), 5))
    assert chunks == [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11]]

    # `emoji` is not in # PKGS: and therefore tests automatic import-name lookup.
    print(emoji.emojize(":rocket: automatic fallback installed", language="alias"))
    print(f"dateutil parsed: {parsed.astimezone(UTC).isoformat()}")
    print(f"more-itertools chunks: {chunks}")


def numpy_report() -> None:
    """Exercise a Pyodide-provided native WASM package."""
    values = np.arange(40_000, dtype=np.float64).reshape(200, 200)
    result = values @ values.T
    print(f"numpy matrix: shape={result.shape}, mean={result.mean():.2f}")


async def run_canvas_test() -> None:
    """Render and animate a bounded Pygame test, with Escape as an early exit."""
    pygame.init()
    width, height = 360, 220
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PyMarklet integration stress test")

    particle_count = 72
    positions = np.random.random((particle_count, 2)) * [width, height]
    velocities = (np.random.random((particle_count, 2)) - 0.5) * 3.5
    colors = np.random.randint(70, 255, size=(particle_count, 3))

    print("canvas: running 180 frames; click canvas and press Escape to stop early")
    for frame in range(180):
        if any(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE for event in pygame.event.get()):
            print("canvas: stopped with Escape")
            break

        positions += velocities
        for axis, boundary in enumerate((width, height)):
            outside = (positions[:, axis] < 4) | (positions[:, axis] > boundary - 4)
            velocities[outside, axis] *= -1
            positions[:, axis] = np.clip(positions[:, axis], 4, boundary - 4)

        screen.fill((15, 18, 26))
        for position, color in zip(positions, colors, strict=True):
            pygame.draw.circle(screen, tuple(int(value) for value in color), tuple(int(value) for value in position), 4)
        pygame.display.flip()

        if frame % 60 == 0:
            print(f"canvas: rendered frame {frame}")
        await asyncio.sleep(1 / 60)

    # Pyodide's Pygame backend is attached to the browser event loop. Calling
    # pygame.quit() here tears down that backend while the callback is active.
    print("canvas: completed")


async def main() -> None:
    print("=== PYMARKLET GENERATOR INTEGRATION STRESS TEST ===")
    dependency_report()
    numpy_report()
    print(await fetch_status())
    await run_canvas_test()
    print("=== STRESS TEST COMPLETED ===")


asyncio.create_task(main())
