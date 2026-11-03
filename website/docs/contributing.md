---
sidebar_position: 8
title: Contributing
description: Set up a development environment, run tests, and build the docs.
---

# Contributing

Thanks for helping improve PyMarklet. This page covers development setup,
checks, and documentation builds.

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
update tests alongside any behavior change. CI runs the suite on Python 3.11
through 3.14.

## Building and checking the package

```sh
uv build
uvx twine check dist/*
```

`dist/` is git-ignored; rebuild it rather than committing artifacts.

## Manual integration testing

The generator's output is JavaScript that runs in a browser, so unit tests
cannot cover the full path. To exercise it end to end:

```sh
uv run pymarklet examples/integration_stress_test.py
```

Open `examples/sandbox.html` in a browser and activate the generated bookmarklet
on that page. Network access is required, since Pyodide is fetched from jsDelivr
at runtime.

## Documentation

The documentation site is built with [Docusaurus](https://docusaurus.io/) from
the `website/` directory.

```sh
cd website
npm install
npm run start
```

The development server opens at `http://localhost:3000`. Most changes reload
automatically.

To produce a production build:

```sh
cd website
npm ci
npm run build
```

The static output is written to `website/build`.

### Read the Docs

The [`.readthedocs.yaml`](https://github.com/Block120/PyMarklet/blob/main/.readthedocs.yaml)
file configures a custom Read the Docs build:

- Node.js 22 is installed as a build tool.
- `npm ci` and `npm run build` run inside `website/`.
- The contents of `website/build` are copied to
  `$READTHEDOCS_OUTPUT/html/`.

The Docusaurus config derives `url` and `baseUrl` from
`READTHEDOCS_CANONICAL_URL`, so the same build works locally and under Read the
Docs versioned paths such as `/en/latest/`. Keep `trailingSlash: true` unless you
also update the Read the Docs routing.

When you add or rename a doc, update `website/sidebars.ts` and check for broken
links. The production build fails on broken links.

## Making a change

1. Keep changes focused. Prefer fixing the root cause over a surface-level
   patch, and match the surrounding style.
2. Update the README, tests, and documentation when your change affects
   documented behavior or adds a feature.
3. Run the test suite and the package build before opening a pull request.
4. Open a pull request against `main` describing what changed and why. Link any
   relevant issue.

## Reporting bugs and vulnerabilities

- General bugs and feature requests: open a
  [GitHub issue](https://github.com/Block120/PyMarklet/issues).
- Security problems: follow [Security and privacy](./security.md); do not open a
  public issue.

## Project layout

```text
src/pymarklet/
  cli.py          command-line entry point
  generator.py    bookmarklet builder and import inspection
tests/            unittest suite
examples/         manual integration example and sandbox page
website/          Docusaurus documentation site
```
