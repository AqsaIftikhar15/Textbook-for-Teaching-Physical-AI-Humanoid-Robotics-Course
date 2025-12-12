// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/week-1-2-intro-physical-ai',
        'module-1-ros2/week-3-ros2-fundamentals',
        'module-1-ros2/week-4-advanced-ros2'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/week-6-7-gazebo-unity',
        'module-2-digital-twin/simulation-concepts'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3-ai-brain/week-8-10-isaac-platform',
        'module-3-ai-brain/week-11-12-humanoid-dev',
        'module-3-ai-brain/week-13-conversational-robotics'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vla/week-13-vla-concepts',
        'module-4-vla/week-13-vla-intro',
        'module-4-vla/week-14-voice-command-intro',
        'module-4-vla/multimodal-integration-challenges',
        'module-4-vla/cross-modal-attention-math',
        'module-4-vla/gpt-model-applications',
        'module-4-vla/cognitive-planning-voice-commands',
        'module-4-vla/language-model-math',
        'module-4-vla/hri-design-principles-intro',
        'module-4-vla/hri-speech-recognition',
        'module-4-vla/gesture-vision-integration',
        'module-4-vla/multimodal-fusion-math',
        'module-4-vla/llm-possibilities-intro',
        'module-4-vla/llm-limitations-robot-control',
        'module-4-vla/llm-safety-considerations',
        'module-4-vla/llm-uncertainty-math',
        'module-4-vla/vla-index',
        'module-4-vla/vla-glossary',
        'module-4-vla/quick-reference-guides',
        'module-4-vla/phase-7-validation'
      ],
    },
  ],
};

module.exports = sidebars;