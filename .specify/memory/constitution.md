<!--
Sync Impact Report:
Version change: 1.0.0 → 1.0.1 (Phase 2: Integrated RAG Chatbot Development addition)
Modified principles: N/A (appended new section)
Added sections: Phase 2: Integrated RAG Chatbot Development
Removed sections: N/A
Templates requiring updates: N/A
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

## Phase 2: Integrated RAG Chatbot Development

### Core Principles for RAG Chatbot

#### Content Accuracy and Relevance
All chatbot responses must be strictly based on book content. Responses must cite specific chapters, sections, or pages when referencing book material. The chatbot must not generate hallucinated information or content outside the scope of the book. Responses must maintain the same technical accuracy standards as the rest of the book content.

#### Privacy and User Query Handling
User queries must be treated as confidential and not stored permanently. Query logs may only be retained for debugging and improvement purposes with appropriate anonymization. Personal information contained in queries must be protected according to privacy best practices.

#### Technical Clarity and Accessibility
Chatbot responses must maintain the same accessibility standards as the book content (Flesch-Kincaid Grade 10–12). Responses should be tailored to intermediate students with Python, ML, and AI backgrounds. Complex concepts must be explained with appropriate context and examples drawn from book content.

### Technical Standards for RAG Implementation

#### Backend Development Standards
Backend services must use FastAPI framework with proper async/await patterns for scalability. API endpoints must follow RESTful principles with appropriate HTTP status codes. Type hints must be used throughout for better maintainability. Proper error handling and validation must be implemented for all endpoints.

#### Vector Store Integration
Vector storage must utilize Qdrant Cloud Free Tier with proper configuration for document chunking and retrieval. Embedding models must be compatible with the vector store schema. Search algorithms must support semantic similarity with configurable thresholds. Proper indexing strategies must be implemented for efficient retrieval.

#### OpenAI Agents Usage
OpenAI API integration must follow best practices for rate limiting and error handling. Prompt engineering must ensure responses are grounded in book content. Response streaming should be implemented for better user experience. Proper API key management and security must be enforced.

#### Frontend Integration Standards
Chatbot widget must be seamlessly integrated into Docusaurus pages without disrupting existing functionality. Responsive design must ensure compatibility across devices. Loading states and error handling must be properly implemented. The integration must not affect page load times or performance significantly.

#### Logging and Error Handling
All chatbot interactions must be logged with appropriate detail levels for debugging. Error logs must include sufficient context for troubleshooting without exposing sensitive information. Response reproducibility must be ensured through proper session tracking and query logging. Performance metrics must be collected for monitoring and optimization.

### Development Workflow for Chatbot Features

#### Integration Testing
All chatbot features must undergo integration testing with existing book content. Response accuracy must be validated against known book information. User interaction flows must be tested end-to-end. Performance benchmarks must be established and maintained.

#### Quality Assurance for Responses
Responses must be validated for technical accuracy against book content. Hallucination detection must be implemented and monitored. Relevance scoring must be applied to ensure responses address user queries appropriately. Moderation systems must prevent inappropriate content generation.

#### Deployment Standards
Chatbot deployment must follow the same CI/CD pipeline as the main book site. Backend services must be deployed with appropriate monitoring and alerting. Frontend integration must be tested across all supported browsers and devices. Rollback procedures must be established for chatbot-specific features.

### Governance for Chatbot Contributions

#### Contribution Standards
All RAG chatbot contributions must follow the same review process as existing book content. Technical accuracy must be verified by domain experts. Code contributions must pass the same quality standards as the rest of the project. Documentation must be maintained for all chatbot-specific features.

#### Frontend Modification Governance
Any modifications to the frontend must preserve the four-module architecture and existing content structure. Navigation and user experience must remain consistent with the rest of the book. Changes must not negatively impact existing Docusaurus functionality or deployment processes.

#### Content Override Mechanism
User-selected text functionality must be implemented to override general search context appropriately. The override mechanism must maintain the same accuracy and citation standards as general queries. Proper validation must ensure user selections are handled securely and accurately.

**Version**: 1.0.1 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-13