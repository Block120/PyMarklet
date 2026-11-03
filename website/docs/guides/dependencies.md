---
sidebar_position: 1
title: Dependencies
description: How PyMarklet detects imports, loads Pyodide packages, and installs PyPI distributions.
---

# Dependencies

Your script can import third-party packages, but everything must run under
Pyodide in the browser. PyMarklet resolves dependencies in three stages when the
bookmarklet starts.

## How resolution works

1. **Pyodide's import scan.** The loader calls
   `pyodide.loadPackagesFromImports(pyCode)`, which inspects normal `import`
   statements and loads packages that Pyodide recognizes from its own
   distribution. This covers the standard library and many prebuilt packages,
   such as NumPy and Pygame.
2. **Declared distributions.** Packages listed in a first-line `# PKGS:`
   manifest are installed with `micropip`. This is how you name a PyPI
   distribution whose import name differs from the distribution name.
3. **Import-name fallback.** For each detected top-level absolute import that is
   still missing, the loader checks `importlib.util.find_spec` and tries to
   install a PyPI package with the same name. This automatically handles
   packages such as `emoji` where the import name and distribution name match.

Declared packages are installed before the fallback check, so a correctly
declared distribution is not installed twice.

## The `# PKGS:` manifest

Add a comment on the **first line** of your script listing PyPI distribution
names:

```python
# PKGS: python-dateutil, more-itertools
from dateutil import parser
from more_itertools import chunked

print(parser.isoparse("2026-10-10T12:34:56Z"))
print(list(chunked(range(6), 2)))
```

Rules:

- The manifest must be on the first line. A blank line before it disables it.
- `# PKGS:` is case-insensitive; `# pkgs:` works too.
- Entries are comma-separated and surrounding whitespace is trimmed.
- Empty entries are ignored and duplicates are removed in first-seen order.
- Each entry may be a normal PyPI requirement specifier, such as
  `requests>=2.32` or `idna==3.7`.

### Import names that differ from distribution names

Use the manifest whenever the import name is not the distribution name:

```python
# PKGS: scikit-learn, beautifulsoup4, pillow
from sklearn.ensemble import RandomForestClassifier
from bs4 import BeautifulSoup
from PIL import Image

print(RandomForestClassifier.__name__, BeautifulSoup.__name__, Image.__name__)
```

Common pairs include:

| Import name | PyPI distribution |
| --- | --- |
| `dateutil` | `python-dateutil` |
| `more_itertools` | `more-itertools` |
| `sklearn` | `scikit-learn` |
| `bs4` | `beautifulsoup4` |
| `PIL` | `pillow` |

If the import name matches the distribution name, you usually do not need the
manifest — the fallback installs it automatically. Declaring it anyway is
harmless and makes the dependency explicit.

## Static detection limits

Import detection is best-effort and deliberately static:

- **Not detected:** dynamic imports such as
  `importlib.import_module("name")` or `__import__("name")`.
- **Not detected:** relative imports such as `from .local import helper`.
- **Detected:** top-level and nested `import` / `from ... import` statements,
  including imports inside functions and conditionals.
- **Passed through:** a script with a syntax error produces no detected imports;
  Pyodide reports the original syntax error when the bookmarklet runs.

When detection fails, add the distribution to `# PKGS:`.

## Pyodide compatibility

Only packages with Pyodide-compatible wheels can run. `micropip` can install
pure-Python wheels directly; packages with native extensions must have a
WebAssembly build available for the pinned Pyodide version. Packages that rely
on desktop-only APIs, subprocesses, or unsupported native libraries will not
work even if they install.

Built-in Pyodide packages do not need to be declared. For example,
`pyodide.http` and `numpy` are part of the runtime distribution.

## Reproducibility and security

Dependencies are downloaded and executed in the browser at runtime. If
reproducibility or supply-chain control matters, pin versions in the manifest:

```python
# PKGS: requests==2.32.3, python-dateutil==2.9.0.post0
```

See [Security and privacy](../security.md) for the broader threat model.

## Next steps

- [Use graphical libraries and the canvas](./graphical-apps.md)
- [Run the integration example](./examples.md)
