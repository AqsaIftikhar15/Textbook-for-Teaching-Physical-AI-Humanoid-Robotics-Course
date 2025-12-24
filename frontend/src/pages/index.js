import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';
import ChatWidget from '../components/ChatWidget'; // import your chat widget

export default function Home() {
  // Staggered animation delays for module cards
  const modules = [
    {
      title: "Module 1: ROS 2",
      description: "The robotic nervous system and middleware architecture",
      link: "/docs/module-1-ros2/week-1-2-intro-physical-ai",
      delay: 0.2,
    },
    {
      title: "Module 2: Digital Twin",
      description: "Simulation using Gazebo and Unity",
      link: "/docs/module-2-digital-twin/week-6-7-gazebo-unity",
      delay: 0.4,
    },
    {
      title: "Module 3: AI Brain",
      description: "NVIDIA Isaac, perception, and navigation",
      link: "/docs/module-3-ai-brain/week-8-10-isaac-platform",
      delay: 0.6,
    },
    {
      title: "Module 4: VLA",
      description: "Vision-Language-Action and multimodal robotics",
      link: "/docs/module-4-vla/week-13-vla-concepts",
      delay: 0.8,
    },
  ];

  const backendUrl = "https://aqsaiftikhar-physical-ai-book-backend.hf.space"; // your backend URL

  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="An academic book on Physical AI and Humanoid Robotics"
    >
      <main className={styles.main}>
        {/* Hero section */}
        <section className={styles.hero}>
          <h1 style={{ animation: 'slideInDown 1s ease forwards' }}>
            Physical AI & Humanoid Robotics
          </h1>
          <p style={{ animation: 'fadeIn 1.5s ease forwards' }}>
            A structured academic book covering humanoid robotics systems,
            simulation, and AI integration.
          </p>

          <Link
            className="button button--primary button--lg"
            to="/docs"
            style={{ animation: 'fadeIn 2s ease forwards', animationDelay: '0.5s' }}
          >
            Read the Full Book
          </Link>
        </section>

        {/* Modules */}
        <section className={styles.modules}>
          {modules.map((mod, idx) => (
            <Module
              key={idx}
              title={mod.title}
              description={mod.description}
              link={mod.link}
              delay={mod.delay}
            />
          ))}
        </section>

        {/* Chat Widget */}
        <section style={{ marginTop: '2rem' }}>

          <ChatWidget  
            fullBookEndpoint={`https://aqsaiftikhar-physical-ai-book-backend.hf.space/query/full`}
            selectedTextEndpoint={`https://aqsaiftikhar-physical-ai-book-backend.hf.space/query/selected`}
            bookId="5ad75c79-c6de-497f-81f5-7cb94a4c50db"
            />

        </section>
      </main>
    </Layout>
  );
}

function Module({ title, description, link, delay }) {
  return (
    <div
      className={styles.card}
      style={{
        animation: 'fadeIn 1s ease forwards',
        animationDelay: `${delay}s`,
      }}
    >
      <h3>{title}</h3>
      <p>{description}</p>
      <Link className="button button--secondary button--sm" to={link}>
        View Module
      </Link>
    </div>
  );
}
