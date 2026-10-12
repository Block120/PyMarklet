# Security Policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub's
[security advisory form](https://github.com/Block120/PyMarklet/security/advisories/new).
Do not open a public issue for a security problem.

Include as much of the following as you can:

- A description of the issue and its impact.
- Steps to reproduce it, including the Python source, the command used, and
  whether the problem is in the generator or in the generated bookmarklet.
- The affected version and your Python and browser versions.

We will acknowledge your report as soon as we can and coordinate a fix and
disclosure timeline with you.

## Supported versions

PyMarklet is pre-1.0 and only the latest published release is supported. Please
reproduce issues on the most recent version before reporting.

## Scope

PyMarklet is a code generator. The relevant security surface has two parts:

1. **The `pymarklet` CLI and library**, which read a Python file and write a
   `javascript:` bookmarklet URL.
2. **Generated bookmarklets**, which embed your Python source and run it with
   [Pyodide](https://pyodide.org/) inside whichever page activates them.

Two properties are intentional and are not vulnerabilities on their own:

- **Source is embedded in the URL.** Anyone who has a bookmarklet can decode and
  read the Python source it contains. Never put secrets, credentials, or
  sensitive data in scripts you turn into bookmarklets.
- **Code runs in the page's context.** A bookmarklet executes with the
  permissions and network environment of the page where it is activated. Only
  run bookmarklets from sources you trust, and only on pages where injected code
  is appropriate.

Report instead, for example: generator bugs that let forged input escape the
embedded data, integrity problems with the pinned Pyodide runtime, or ways a
bookmarklet could execute code beyond what its embedded source specifies.

## Dependencies and runtime

Generated bookmarklets load **Pyodide** from jsDelivr and may install packages
from PyPI-compatible hosts at runtime. Whether those fetches succeed depends on
the page's Content Security Policy, ad blockers, and network. If you need
reproducibility or supply-chain control, pin requirement versions in the
first-line `# PKGS:` manifest. See the README's *Security and privacy* section
for details.
