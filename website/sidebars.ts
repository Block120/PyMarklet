import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Getting started',
      collapsed: false,
      items: [
        'getting-started/installation',
        'getting-started/quickstart',
        'getting-started/writing-scripts',
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      collapsed: false,
      items: [
        'guides/dependencies',
        'guides/graphical-apps',
        'guides/examples',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      collapsed: false,
      items: ['reference/cli', 'reference/python-api', 'reference/runtime'],
    },
    'limitations',
    'security',
    'faq',
    'contributing',
  ],
};

export default sidebars;
