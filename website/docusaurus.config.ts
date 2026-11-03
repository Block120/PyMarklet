import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// Read the Docs sets READTHEDOCS_CANONICAL_URL to the canonical address of the
// version being built, for example https://pymarklet.readthedocs.io/en/latest/.
// Docusaurus needs the origin and the path separately, so split them here.
const canonicalUrl =
  process.env.READTHEDOCS_CANONICAL_URL ?? 'https://pymarklet.readthedocs.io/';
const canonical = new URL(canonicalUrl);
const baseUrl = canonical.pathname.endsWith('/')
  ? canonical.pathname
  : `${canonical.pathname}/`;

const repoUrl = 'https://github.com/Block120/PyMarklet';

const config: Config = {
  title: 'PyMarklet',
  tagline: 'Turn a Python script into a browser bookmarklet',
  favicon: 'img/logo.svg',

  future: {
    v4: true,
  },

  url: canonical.origin,
  baseUrl,

  // Read the Docs serves versioned paths with a trailing slash. Keeping this on
  // avoids routing loops between Docusaurus and the Read the Docs proxy.
  trailingSlash: true,

  organizationName: 'Block120',
  projectName: 'PyMarklet',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: `${repoUrl}/edit/main/website/`,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'PyMarklet',
      logo: {
        alt: 'PyMarklet logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docs',
          position: 'left',
          label: 'Documentation',
        },
        {
          type: 'doc',
          docId: 'reference/python-api',
          position: 'left',
          label: 'Python API',
        },
        {
          href: `${repoUrl}/releases`,
          label: 'Changelog',
          position: 'right',
        },
        {
          href: 'https://pypi.org/project/pymarklet/',
          label: 'PyPI',
          position: 'right',
        },
        {
          href: repoUrl,
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Getting started', to: '/docs/getting-started/installation'},
            {label: 'Dependencies', to: '/docs/guides/dependencies'},
            {label: 'CLI reference', to: '/docs/reference/cli'},
            {label: 'Python API', to: '/docs/reference/python-api'},
          ],
        },
        {
          title: 'Project',
          items: [
            {label: 'GitHub', href: repoUrl},
            {label: 'Issue tracker', href: `${repoUrl}/issues`},
            {label: 'PyPI', href: 'https://pypi.org/project/pymarklet/'},
            {label: 'Contributing', to: '/docs/contributing'},
          ],
        },
        {
          title: 'More',
          items: [
            {label: 'Examples', to: '/docs/guides/examples'},
            {label: 'Limitations', to: '/docs/limitations'},
            {label: 'Security and privacy', to: '/docs/security'},
            {label: 'FAQ', to: '/docs/faq'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} PyMarklet contributors. Built with Docusaurus and hosted on Read the Docs.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'python'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 3,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
