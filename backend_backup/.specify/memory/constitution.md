<!-- SYNC IMPACT REPORT:
Version change: 0.1.0 → 1.0.0
Added principles: Spec-Driven Development, Accuracy and Faithfulness, Contextual Relevance, Security and Efficiency, Code Quality, Cost-effectiveness
Modified principles: None
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.toml ⚠ pending
Runtime docs requiring updates: README.md ⚠ pending
-->

# Integrated RAG Chatbot Constitution

## Core Principles

### I. Spec-Driven Development
Spec-driven development prioritizing clear, verifiable specifications before implementation. All features must have comprehensive specifications detailing acceptance criteria before any implementation begins. This ensures predictable development cycles and clear definition of done.

### II. Accuracy and Faithfulness
High accuracy and faithfulness to the book's content in all chatbot responses. The system must maintain strict adherence to source material without fabricating information or introducing inaccuracies. This ensures trustworthiness and reliability of the knowledge base.

### III. Contextual Relevance
Support both full-book queries and precise answers based solely on user-selected text passages. The system must distinguish between general knowledge retrieval and targeted, context-limited responses with no hallucination from outside the selected text.

### IV. Security, Privacy, and Efficiency
Secure and efficient data handling practices for all content processing and retrieval operations. System must protect user data and book content while maintaining optimal performance characteristics and resource utilization.

### V. Clean and Maintainable Code
Clean, maintainable, and well-documented code following Python best practices. All code must include comprehensive documentation, type hints, and follow established style guidelines to ensure long-term maintainability.

### VI. Cost-Effective Reliability
Use cost-effective and reliable technology solutions leveraging free tiers where possible without compromising quality. Solutions must be sustainable within budget constraints while maintaining dependable performance.

## Technology Stack Requirements

All implementations must comply with the following technology requirements:
- Use Cohere API exclusively for embeddings and generation (no OpenAI)
- Vector storage and search: Qdrant Cloud Free Tier
- Metadata storage and session management: Neon Serverless Postgres
- Backend framework: FastAPI with async support and proper error handling
- Embedding model: Cohere multilingual or embed-english-v3.0
- Generation model: Cohere Command R or R+
- All API keys and secrets managed via environment variables

## Content Processing Standards

- Chunking strategy: Semantic or overlapping chunks for optimal retrieval quality
- RAG pipeline: Embed with Cohere, store in Qdrant with metadata linking to Postgres if needed
- Book content ingestion: Support PDF/HTML/text upload and chunking
- Embedding format: Interactive widget allowing text selection with isolated RAG query

## Quality Assurance

All components must include comprehensive testing:
- Unit tests for key components (ingestion, retrieval, query)
- Performance benchmarks with sub-second response times
- End-to-end verification: Ingest book → Query full book → Query selected passage
- Manual verification on sample questions to prevent hallucination

## Governance

This constitution supersedes all other development practices for the Integrated RAG Chatbot project. All code changes, architectural decisions, and feature implementations must be verified for constitutional compliance. Amendments to this constitution require documented approval and migration planning.

**Version**: 1.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-12-19
