# Contributing to PyMarklet

Thanks for helping improve PyMarklet. This document covers setting up a
development environment, running the checks, and submitting changes.

## Development setup

PyMarklet uses [uv](https://docs.astral.sh/uv/) for dependency management and
building. The package has no runtime dependencies; Python 3.11 or later is
required.

```sh
uv sync
```

## Running the tests

```sh
uv run python -m unittest discover -s tests -v
```

Tests live in `tests/` and use the standard library `unittest` framework. Add or
update tests alongside any behavior change. The CI workflow runs the suite on
Python 3.11 through 3.14.

## Building the package

```sh
uv build
uvx twine check dist/*
```

`dist/` is git-ignored; rebuild it rather than committing artifacts.

## Making a change

1. Keep changes focused. Prefer fixing the root cause over a surface-level
   patch, and match the surrounding style.
2. Update the README and `tests/` when your change affects documented behavior
   or adds a feature.
3. Run the test suite and the build before opening a pull request.
4. Open a pull request against `main` describing what changed and why. Link any
   relevant issue.

## Manual integration testing

The generator's output is JavaScript that runs in a browser, so unit tests
cannot cover the full path. To exercise it end to end:

```sh
pymarklet examples/integration_stress_test.py
```

Open `examples/sandbox.html` in a browser and activate the generated bookmarklet
on that page. Network access is required, since Pyodide is fetched from jsDelivr
at runtime.

## Reporting bugs and vulnerabilities

- General bugs and feature requests: open a
  [GitHub issue](https://github.com/Block120/PyMarklet/issues).
- Security problems: follow [`SECURITY.md`](SECURITY.md); do not open a public
  issue.
