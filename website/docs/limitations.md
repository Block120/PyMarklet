---
sidebar_position: 5
title: Limitations
description: What PyMarklet cannot do, and why.
---

# Limitations

PyMarklet is experimental. Know these constraints before relying on it.

## Network access is required

The browser fetches Pyodide from jsDelivr and may fetch packages from
PyPI-compatible hosts. Offline use, blocked CDNs, and restrictive proxies all
prevent the bookmarklet from starting.

## Content Security Policy can block execution

Sites may block the injected Pyodide script, package downloads, or required
browser APIs. In the strictest cases, activating the bookmarklet does nothing
visible. There is no way to bypass a page's CSP from a bookmarklet.

## Only Pyodide-compatible packages work

Native packages without WebAssembly wheels cannot be installed. Pure-Python
wheels generally work through `micropip`, but packages that require unsupported
native libraries, subprocesses, or desktop-only APIs will fail even if they
install. See [Dependencies](./guides/dependencies.md).

## Import detection is static and best-effort

The generator parses your script with `ast` and records top-level absolute
imports. Dynamic imports and relative imports are not detected. When detection
misses a dependency, declare it in the first-line `# PKGS:` manifest.

## Bookmark URLs have practical length limits

The loader is already several thousand characters long, and the URL grows
roughly with your script. Browsers and bookmark sync services may truncate or
reject long URLs. Keep scripts small and store data externally when possible.

## Python runs in the page, not in a sandbox

A bookmarklet executes with the permissions and network environment of the page
where you activate it. It is not a security boundary. Only run bookmarklets you
trust, and only on pages where injected code is appropriate.

## Closing the panel does not stop Python

Clicking **×** removes the UI but does not forcibly cancel Python work already
scheduled in the page. Reload the page to discard the runtime.

## Pinned runtime

Each PyMarklet release pins a Pyodide version — currently `0.27.5`. Regenerate
bookmarklets after upgrading the generator to pick up the new pin and any
generator fixes.

## Next steps

- [Security and privacy](./security.md)
- [Frequently asked questions](./faq.md)
