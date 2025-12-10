// @ts-check
// `ts-check` enables type checking for the config file
// Note: type checking is not enabled for JavaScript files by default

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Understanding Humanoid Robot Systems from Middleware to Multimodal AI Integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://aqsaiftikhar15.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages, this is usually '/<projectName>/'
  baseUrl: '/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Aqsa Iftikhar', // Usually your GitHub org/user name.
  projectName: 'Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/',
        },
        blog: false, // Optional: disable the blog plugin
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Robotics Book Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Modules',
          },
          {
            href: 'https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: The Robotic Nervous System (ROS 2)',
                to: '/docs/module-1-ros2/week-1-2-intro-physical-ai',
              },
              {
                label: 'Module 2: The Digital Twin (Gazebo & Unity)',
                to: '/docs/module-2-digital-twin/week-6-7-gazebo-unity',
              },
              {
                label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
                to: '/docs/module-3-ai-brain/week-8-10-isaac-platform',
              },
              {
                label: 'Module 4: Vision-Language-Action (VLA)',
                to: '/docs/module-4-vla/week-13-vla-concepts',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),
};

module.exports = config;