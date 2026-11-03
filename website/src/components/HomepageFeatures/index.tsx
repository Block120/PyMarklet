import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const TerminalIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect x="3" y="4" width="18" height="16" rx="2" />
    <path d="m7 9 3 3-3 3" />
    <path d="M13 15h4" />
  </svg>
);

const BrowserIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect x="2.5" y="4" width="19" height="16" rx="2" />
    <path d="M2.5 8.5h19" />
    <circle cx="5.5" cy="6.25" r="0.75" fill="currentColor" stroke="none" />
    <circle cx="8" cy="6.25" r="0.75" fill="currentColor" stroke="none" />
    <path d="m9 12-2 2 2 2M15 12l2 2-2 2M13 11l-2 6" />
  </svg>
);

const PackageIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <path d="m12 3 9 4.5v9L12 21l-9-4.5v-9z" />
    <path d="M3 7.5 12 12l9-4.5M12 12v9" />
    <path d="m7.5 5.25 9 4.5" />
  </svg>
);

const CanvasIcon = (props: React.ComponentProps<'svg'>) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" {...props}>
    <rect x="2.5" y="4" width="19" height="14" rx="2" />
    <path d="M9 22h6M12 18v4" />
    <circle cx="8" cy="9" r="1.25" />
    <path d="m4.5 16 4.5-4 3 2.5L15 11l4.5 5" />
  </svg>
);

const FeatureList: FeatureItem[] = [
  {
    title: 'One command',
    Svg: TerminalIcon,
    description: (
      <>
        Point <code>pymarklet</code> at a Python file and get a{' '}
        <code>javascript:</code> URL. No extension, server, or config file.
      </>
    ),
  },
  {
    title: 'Python in the browser',
    Svg: BrowserIcon,
    description: (
      <>
        Your source is embedded in the bookmark and runs with Pyodide 0.27.5 in
        WebAssembly on any page you trust.
      </>
    ),
  },
  {
    title: 'Dependencies handled',
    Svg: PackageIcon,
    description: (
      <>
        Imports are detected, Pyodide packages are loaded, and missing
        distributions can be installed from PyPI at runtime.
      </>
    ),
  },
  {
    title: 'Graphics-ready',
    Svg: CanvasIcon,
    description: (
      <>
        A wired-up canvas lets Pygame and other canvas-aware libraries draw
        inside the draggable output panel.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--3', styles.feature)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" aria-hidden="true" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
