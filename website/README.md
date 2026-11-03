# PyMarklet documentation website

The documentation site is built with [Docusaurus](https://docusaurus.io/) and
deployed with [Read the Docs](https://readthedocs.org/). Content lives in
`docs/`; navigation is defined in `sidebars.ts`.

## Requirements

- Node.js 20 or later (Read the Docs uses Node.js 22)
- npm

## Local development

```bash
npm ci
npm run start
```

The site opens at <http://localhost:3000>. Most content changes reload
automatically.

## Build

```bash
npm ci
npm run build
```

Static output is written to `build/`. The production build treats broken links
as errors, so run it before opening a pull request that changes documentation.

To serve the production build locally:

```bash
npm run serve
```

## Read the Docs

The repository-level `.readthedocs.yaml` runs a custom build:

1. Install Node.js 22.
2. Run `npm ci` and `npm run build` in `website/`.
3. Copy `website/build` into `$READTHEDOCS_OUTPUT/html/`.

`docusaurus.config.ts` reads `READTHEDOCS_CANONICAL_URL` to set `url` and
`baseUrl`, so the same build works locally (at the site root) and on Read the
Docs versioned paths such as `/en/latest/`. Keep `trailingSlash: true` unless
the Read the Docs routing is updated as well.

## Structure

```text
docs/
  intro.md
  getting-started/    install, quick start, writing scripts
  guides/             dependencies, graphics, examples
  reference/          CLI, Python API, generated runtime
  limitations.md
  security.md
  faq.md
  contributing.md
src/
  components/         landing-page feature grid
  css/custom.css      theme overrides
  pages/index.tsx     landing page
static/img/           logo and favicon
```
