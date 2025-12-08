<!--
Sync Impact Report:
Version change: N/A → 1.0.0 (initial creation)
Modified principles: N/A
Added sections: All principles and sections for Physical AI & Humanoid Robotics project
Removed sections: N/A
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - needs alignment check
- ✅ .specify/templates/spec-template.md - needs alignment check
- ✅ .specify/templates/tasks-template.md - needs alignment check
- ✅ .specify/templates/commands/*.md - needs review for generic guidance
- ✅ README.md - needs update for project-specific guidance
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### Technical Accuracy and Source Verification
All factual claims must be traceable to credible primary sources. Minimum 60% peer-reviewed sources required. Zero plagiarism tolerance. All information must be verifiable through peer-reviewed robotics & AI papers, open-source robotics documentation (ROS2, Gazebo, Isaac Sim, MuJoCo), or industry research (Boston Dynamics, Tesla Optimus, Figure AI, Unitree).

### Clarity for Intermediate Students
Content must be accessible to students with intermediate Python, ML, and AI background. Writing clarity follows Flesch-Kincaid Grade 10–12 standard. All code examples must be executable and documented. All diagrams must be explained conceptually and mathematically.

### Embodied Intelligence Focus
Content emphasizes the bridge between digital brain and physical body. All robotics pipelines must include: Sensors → Perception → Decision → Control → Actuators. Focus on perception → cognition → actuation flow. Simulation-to-reality transfer (Sim2Real) must be explicitly addressed.

### Reproducibility and Open Source
All experiments and models must be reproducible. Code examples must be executable. All simulations must be reproducible. Open-source learning philosophy must be maintained throughout all content and examples.

### Four-Module Architecture
All content must fit within exactly four primary modules: (1) Robotic Nervous System (ROS 2), (2) Digital Twin (Gazebo & Unity), (3) AI-Robot Brain (NVIDIA Isaac™), (4) Vision-Language-Action (VLA). No chapters may exist outside these four modules.

### Safety and Validation
All AI models must include: Dataset description, Training loop, Evaluation metrics. All control systems must include: Kinematics, Dynamics, Feedback control. Safety rules must be included for all real-world robotics sections.

## Technical Standards

### Documentation Standard
Documentation must follow Docusaurus standards as specified at https://docusaurus.io/docs. Book framework uses Docusaurus (latest version). Deployment via GitHub Pages. All technical content must adhere to established robotics and AI documentation standards.

### Code Quality Requirements
Code languages include: Python for AI & robotics control, ROS2 for robot middleware, PyTorch for models, Gym / Isaac Sim / MuJoCo for simulation. All code must be documented, tested, and follow established best practices for robotics development.

### Citation and Academic Standards
Citation format follows APA style. Source types include peer-reviewed papers, open-source documentation, and industry research. All factual claims must be traceable. Writing must maintain academic rigor while remaining accessible.

## Development Workflow

### Module-Based Development
Development follows the four-module architecture strictly. Each module represents a functional layer of an embodied humanoid AI system. Content development must align with the specific focus of each module: ROS 2 integration, physics simulation, AI perception/training, and vision-language-action integration.

### Quality Assurance Process
Every robotics pipeline must include sensors, perception, decision, control, and actuators. All control systems must include kinematics, dynamics, and feedback control. All AI models must include dataset description, training loop, and evaluation metrics. Sim2Real gap must be explicitly addressed in all relevant sections.

### Build and Deployment Standards
Book must build successfully using Docusaurus. Site must deploy correctly on GitHub Pages. All chapters must compile without errors. All code samples must be runnable. Repository must follow docs-as-code principles with version-controlled chapters and automated build & deploy.

## Governance

All development must strictly adhere to the four-module architecture. Content must maintain technical accuracy through verified sources. Academic standards must be maintained throughout. Any deviation from the four-module structure requires explicit approval. All contributions must pass technical review by domain experts. Version control follows docs-as-code principles with proper branching and review processes.

**Version**: 1.0.0 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-08