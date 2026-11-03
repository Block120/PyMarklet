---
sidebar_position: 6
title: Security and privacy
description: Threat model, embedded source, and how to report vulnerabilities.
---

# Security and privacy

PyMarklet is a code generator with two parts:

1. **The `pymarklet` CLI and library**, which read a Python file and write a
   `javascript:` bookmarklet URL.
2. **Generated bookmarklets**, which embed your Python source and run it with
   Pyodide inside whichever page activates them.

## Intentional behavior

Two properties are intentional and are not vulnerabilities on their own.

### The source is embedded in the URL

Anyone who has a bookmarklet can decode and read the Python source it contains.
**Never include secrets, credentials, private endpoints, or sensitive data.**
Anyone with the URL can extract the source.

### Code runs in the page's context

A bookmarklet executes with the permissions and network environment of the page
where you activate it. Only run bookmarklets from sources you trust, and only on
pages where injected code is appropriate.

## Practical guidance

- A bookmarklet is executable code. Only run bookmarklets you trust.
- Review site policies before running injected code on a page.
- Pin or constrain dependency versions in `# PKGS:` when reproducibility
  matters. Dependencies are downloaded and executed in the browser.
- PyMarklet relies on jsDelivr to serve its pinned Pyodide runtime. Ad blockers,
  offline mode, proxies, or supply-chain policy may block it.
- Treat a bookmarklet URL like source code: it may contain your logic and any
  data you embedded.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub's
[security advisory form](https://github.com/Block120/PyMarklet/security/advisories/new).
Do not open a public issue for a security problem.

Include as much of the following as you can:

- A description of the issue and its impact.
- Steps to reproduce it, including the Python source, the command used, and
  whether the problem is in the generator or in the generated bookmarklet.
- The affected version and your Python and browser versions.

Examples of issues worth reporting:

- Generator bugs that let forged input escape the embedded data.
- Integrity problems with the pinned Pyodide runtime.
- Ways a bookmarklet could execute code beyond what its embedded source
  specifies.

## Supported versions

PyMarklet is pre-1.0 and only the latest published release is supported. Please
reproduce issues on the most recent version before reporting.

## Next steps

- [Limitations](./limitations.md)
- [Dependencies](./guides/dependencies.md)
