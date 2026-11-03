---
sidebar_position: 1
title: CLI reference
description: Command-line options for the pymarklet generator.
---

# CLI reference

The `pymarklet` command reads a Python source file and writes a bookmarklet URL.

## Synopsis

```text
pymarklet [-h] [-o OUTPUT] python_file
```

## Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `python_file` | Yes | UTF-8 Python source file to embed. |
| `-o`, `--output` | No | Destination file for the bookmarklet URL. Defaults to `bookmarklet.js` in the current directory. |
| `-h`, `--help` | No | Show the help message and exit. |

## Exit status

| Status | Meaning |
| --- | --- |
| `0` | The bookmarklet was written successfully. |
| `1` | The source could not be read or the output file could not be written. An error is printed to standard output. |
| `2` | `argparse` rejected the arguments, such as a missing `python_file`. |

## Output

On success, the command prints:

```text
Bookmarklet written to hello-bookmarklet.txt (12345 characters).
```

The file contains a single `javascript:` URL with no trailing newline. Keep it
intact when copying it into a bookmark.

## Examples

Write to the default output path:

```sh
pymarklet hello.py
```

Write to a named file:

```sh
pymarklet hello.py -o hello-bookmarklet.txt
```

Use a script from another directory:

```sh
pymarklet ~/scripts/report.py -o ~/Downloads/report-bookmarklet.txt
```

The output directory must already exist; PyMarklet does not create parent
directories.

## Errors

Reading problems report the offending path:

```text
Error reading missing.py: [Errno 2] No such file or directory: 'missing.py'
```

Writing problems are reported the same way:

```text
Error writing /read-only/out.txt: [Errno 13] Permission denied: '/read-only/out.txt'
```

## Next steps

- [Python API reference](./python-api.md)
- [Understand the generated runtime](./runtime.md)
