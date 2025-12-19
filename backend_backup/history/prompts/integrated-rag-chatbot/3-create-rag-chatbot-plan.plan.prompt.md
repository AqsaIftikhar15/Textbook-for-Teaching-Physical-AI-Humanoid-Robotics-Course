---
id: 3
title: Create RAG Chatbot Plan
stage: plan
date: 2025-12-19
surface: agent
model: Qwen
feature: integrated-rag-chatbot
branch: 001-integrated-rag-chatbot
user: Qwen
command: /sp.plan
labels: [plan,rag,chatbot,backend]
links:
  spec: specs/001-integrated-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-integrated-rag-chatbot/plan.md
 - specs/001-integrated-rag-chatbot/research.md
 - specs/001-integrated-rag-chatbot/data-model.md
 - specs/001-integrated-rag-chatbot/quickstart.md
 - specs/001-integrated-rag-chatbot/contracts/ingest-api.md
 - specs/001-integrated-rag-chatbot/contracts/query-api.md
 - specs/001-integrated-rag-chatbot/contracts/monitor-api.md
tests:
 - N/A
---

## Prompt

Execute the implementation planning workflow using the plan template to generate design artifacts.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType qwen`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.plan
Project: Integrated RAG Chatbot Embedded in Published Book

Based on the provided /sp.specify and /sp.constitution, create a detailed, phased project plan. Prioritize building a high-accuracy RAG chatbot using Cohere exclusively, with strict faithfulness to the book content and no hallucinations. The plan must adhere strictly to all core principles, key standards, constraints, and success criteria.

Key updates and emphases:
- Initial phases focus exclusively on backend API and ingestion pipeline — no frontend widget development in the core plan.
- Frontend embedding/integration (interactive JS widget for text selection and mobile-responsive chat) will be handled in a separate later phase or project, specifically for integration into a Docusaurus-based digital book.
- Include a dedicated task/phase for a monitoring script to track Qdrant Cloud and Neon Serverless Postgres usage (e.g., collection size, upsert count, query rate, compute usage) to ensure staying within free-tier limits.
- Secure FastAPI backend: Autogenerate Swagger docs, protect all endpoints with API key authentication (e.g., header-based), and implement proper POST endpoints including /query (and variants for ingestion, full-book query, selected-text query).

Structure the plan as follows:
1. **Phases**: Break down into logical, sequential phases (suggested: Project Setup & Environment, Ingestion Pipeline, Vector & Metadata Storage Integration, Secure FastAPI Backend Development, RAG Query Modes Implementation, Monitoring & Usage Tracking, Testing & Verification, Documentation & Demo Preparation). Defer frontend widget to a note as "Future Integration Phase".
2. **Tasks per Phase**: For each phase, list specific, actionable tasks with priorities (High/Medium/Low), estimated effort (hours or days), dependencies, and components (backend-focused).
3. **Milestones**: Define clear, verifiable milestones (e.g., "Secure backend deployed locally: Swagger docs accessible, API key auth enforced, successful full-book query on sample book").
4. **Timeline**: Suggest a realistic yet aggressive timeline assuming heavy iterative development via spec-kit-plus and qwen cli,(ingestion + secure API + both query modes + monitoring).
5. **Resources & Tools**: List required credentials (use provided NEON_DB_URL, QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY via env vars), free-tier limits, and allowed Python packages (e.g., cohere, qdrant-client, psycopg2/asyncpg, fastapi, uvicorn, pydantic, python-dotenv).
6. **Risks & Mitigations**: Highlight risks (e.g., free-tier exhaustion, latency spikes, knowledge bleed between modes, Cohere rate limits) and practical mitigations (e.g., caching, batching, monitoring script alerts).
7. **Iteration Strategy**: Emphasize spec-kit-plus workflow with qwen cli for rapid code generation, refinement, and testing of components.

Key alignments (must preserve):
- Text-only ingestion (PDF/text/HTML) with intelligent semantic/overlapping chunking for high retrieval accuracy.
- Two strictly isolated query modes: Full-book (Qdrant retrieval + Cohere generation) and Selected-text (generation directly on selected passage only, no vector search).
- Cohere only: embed-english-v3.0 or embed-multilingual-v3.0 for embeddings; Command R, R+, or latest series for generation.
- Storage: Qdrant Cloud Free Tier for vectors + payloads; Neon Serverless Postgres for additional metadata (chunk provenance, book versioning).
- Backend: Async FastAPI with proper routing, error handling, rate limiting hints, and security best practices.
- Constraints: No OpenAI, stay strictly within free tiers (Qdrant, Neon, Cohere Trial), Python-only, type-hinted, well-documented code.
- Success criteria: End-to-end backend demo on sample book (upload → ingest → accurate full-book and selected-text queries via POST), latency <2s, non-hallucinated responses, basic tests, usage monitoring.

Ensure the plan is concise, actionable, and promotes clean, secure, production-ready backend code while explicitly deferring frontend embedding to future Docusaurus integration.

## Response snapshot

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

## Outcome

- ✅ Impact: Created comprehensive implementation plan with research, data models, API contracts, and quickstart guide
- 🧪 Tests: N/A
- 📁 Files: specs/001-integrated-rag-chatbot/plan.md, research.md, data-model.md, quickstart.md, contracts/*.md
- 🔁 Next prompts: /sp.tasks to break the plan into specific tasks
- 🧠 Reflection: The plan follows all constitutional principles and includes all required components for the RAG chatbot backend implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown with /sp.tasks
