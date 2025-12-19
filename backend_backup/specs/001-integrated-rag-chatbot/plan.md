# Implementation Plan: Integrated RAG Chatbot

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-19 | **Spec**: [link to spec]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Develop a high-accuracy RAG chatbot that integrates with published books to answer user questions based on full book content or specific selected passages. The system uses Cohere for embeddings and generation, Qdrant for vector storage, and Neon Postgres for metadata management. The backend is built with FastAPI and focuses on accuracy, security, and efficiency while adhering to free-tier constraints.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: cohere, qdrant-client, psycopg2/asyncpg, fastapi, uvicorn, pydantic, python-dotenv, PyMuPDF (fitz) for PDF processing, beautifulsoup4 for HTML processing
**Storage**: Qdrant Cloud (vector storage), Neon Serverless Postgres (metadata)
**Testing**: pytest with unit and integration tests for ingestion, retrieval, and query components
**Target Platform**: Linux/Mac/Windows server environment
**Project Type**: Backend API service
**Performance Goals**: Response latency under 2 seconds for typical queries
**Constraints**: Must stay within Qdrant Cloud Free Tier, Neon Serverless Postgres free tier, and Cohere Trial API limits; no OpenAI usage
**Scale/Scope**: Single book instance per deployment, multiple users accessing the same backend without authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation plan must comply with all core principles from the constitution:

- **Spec-Driven Development**: All components must follow specifications defined in the feature spec
- **Accuracy and Faithfulness**: Responses must be non-hallucinated and faithful to book content
- **Contextual Relevance**: Support both full-book and selected-text query modes
- **Security, Privacy, and Efficiency**: Secure API key handling and efficient resource usage
- **Clean and Maintainable Code**: Well-documented, properly typed Python code following best practices
- **Cost-Effective Reliability**: Stay within free tier limits of all services

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── book.py          # Book entity and chunking logic
│   │   └── query.py         # Query request/response models
│   ├── services/
│   │   ├── ingestion.py     # PDF/HTML/text processing and chunking
│   │   ├── embedding.py     # Cohere embedding service
│   │   ├── storage.py       # Qdrant and Postgres interaction
│   │   └── rag.py           # RAG orchestration service
│   ├── api/
│   │   ├── main.py          # FastAPI app definition
│   │   ├── routes/
│   │   │   ├── ingest.py    # Ingestion endpoints
│   │   │   ├── query.py     # Query endpoints (full-book and selected-text)
│   │   │   └── monitor.py   # Usage monitoring endpoints
│   │   └── middleware/
│   │       └── auth.py      # API key authentication
│   └── config/
│       └── settings.py      # Environment configuration
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── scripts/
│   └── monitor_usage.py     # Script to track Qdrant/Neon usage
├── requirements.txt         # Python dependencies
└── .env.example             # Example environment file
```

**Structure Decision**: Backend API service with clear separation of concerns between models, services, API routes, and configuration. This allows for maintainable, testable code that can be easily deployed and monitored.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phase 0: Outline & Research

### Research Areas:

1. **Cohere API Integration**:
   - Decision: Use Cohere embed-english-v3.0 for embeddings and Command R+ for generation
   - Rationale: These models are specifically required by the specification and provide the best balance of accuracy and cost
   - Alternatives considered: Other embedding models, different generation models

2. **PDF/HTML/Text Processing**:
   - Decision: Use PyMuPDF (fitz) for PDF processing, beautifulsoup4 for HTML parsing
   - Rationale: These libraries provide robust text extraction capabilities with good handling of various formats
   - Alternatives considered: PyPDF2, pdfplumber, lxml

3. **Chunking Strategy**:
   - Decision: Semantic chunking with overlap to maintain context
   - Rationale: This approach preserves meaning while allowing effective retrieval
   - Alternatives considered: Fixed-size chunking, sentence-based chunking

4. **Qdrant Vector Storage**:
   - Decision: Use Qdrant Cloud Free Tier with metadata payload storage
   - Rationale: Required by specification, supports metadata linking to Postgres
   - Alternatives considered: Other vector databases (Pinecone, Weaviate)

## Phase 1: Design & Contracts

### Key Artifacts to Generate:

1. **Data Model** (data-model.md):
   - Book entity: id, title, author, content, chunks
   - Chunk entity: id, text, embedding, metadata, book_id
   - Query entity: request_type, content, response

2. **API Contracts** (contracts/):
   - POST /ingest: Upload and process book files
   - POST /query/full: Query using full book context
   - POST /query/selected: Query using only selected text
   - GET /monitor/usage: Get current usage metrics for free-tier tracking

3. **Quickstart Guide** (quickstart.md):
   - Environment setup instructions
   - Service deployment steps
   - Basic usage examples

## Phase 2: Implementation Phases

### Phase 2A: Project Setup & Environment
- Set up project structure
- Configure environment variables for Cohere, Qdrant, and Neon
- Install and configure dependencies
- Create basic FastAPI app with health check endpoint

### Phase 2B: Ingestion Pipeline
- Implement PDF/HTML/text file upload endpoint
- Create text extraction and preprocessing functions
- Develop semantic chunking with overlap algorithm
- Add validation and error handling for various file formats

### Phase 2C: Vector & Metadata Storage Integration
- Integrate with Cohere for generating embeddings
- Connect to Qdrant Cloud for vector storage
- Set up Neon Postgres for metadata storage
- Implement embedding storage with metadata linking

### Phase 2D: Secure FastAPI Backend Development
- Implement API key authentication middleware
- Create proper request/response models with Pydantic
- Add comprehensive error handling and validation
- Auto-generate Swagger documentation

### Phase 2E: RAG Query Modes Implementation
- Implement full-book query mode using vector search
- Implement selected-text query mode (direct generation on text)
- Add response formatting with citations
- Enforce strict isolation between query modes

### Phase 2F: Monitoring & Usage Tracking
- Create script to monitor Qdrant usage (collection size, upsert count)
- Monitor Neon Postgres usage (compute time, data transfer)
- Add API endpoint to report usage metrics
- Implement alerts when approaching free tier limits

### Phase 2G: Testing & Verification
- Write unit tests for all services
- Create integration tests for end-to-end workflows
- Verify accuracy and faithfulness of responses
- Test both query modes for proper isolation

### Phase 2H: Documentation & Demo Preparation
- Create comprehensive setup documentation
- Prepare sample book for demo
- Document API usage with examples
- Prepare deployment instructions

## Future Integration Phase (Deferred)
- Frontend widget for Docusaurus-based digital books
- Interactive text selection capabilities
- Mobile-responsive chat interface

## Timeline
- Phase A-D (Core Backend): 5-7 days
- Phase E (RAG Implementation): 4-5 days
- Phase F (Monitoring): 2-3 days
- Phase G-H (Testing & Documentation): 3-4 days
- Total estimated: 14-19 days

## Risks & Mitigations
- **Free-tier exhaustion**: Implement usage monitoring and alerts
- **Latency spikes**: Implement caching strategies and consider batch processing
- **Knowledge bleed**: Carefully isolate full-book and selected-text query modes
- **Cohere rate limits**: Implement retry logic and request queuing