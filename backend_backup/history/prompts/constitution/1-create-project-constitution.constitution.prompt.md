---
id: 1
title: Create Project Constitution
stage: constitution
date: 2025-12-19
surface: agent
model: Qwen
feature: none
branch: main
user: Qwen
command: /sp.constitution
labels: [constitution,rag,chatbot,specification]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - N/A
---

## Prompt

Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.

## User Input

```
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

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


/sp.constitution
Project: Integrated RAG Chatbot Embedded in Published Book
Core principles:

Spec-driven development prioritizing clear, verifiable specifications before implementation
High accuracy and faithfulness to the book's content in all chatbot responses
Contextual relevance: Support both full-book queries and precise answers based solely on user-selected text passages
Security, privacy, and efficiency in data handling and retrieval
Clean, maintainable, and well-documented code following Python best practices
Cost-effective and reliable using free tiers where possible

Key standards:

Use Cohere API exclusively for embeddings and generation (no OpenAI)
Vector storage and search: Qdrant Cloud Free Tier
Metadata storage and session management: Neon Serverless Postgres
Backend framework: FastAPI with async support and proper error handling
Chunking strategy: Semantic or overlapping chunks for optimal retrieval quality
RAG pipeline: Embed with Cohere, store in Qdrant with metadata linking to Postgres if needed
Embedding model: Cohere multilingual or embed-english-v3.0
Generation model: Cohere Command R or R+
All API keys and secrets managed via environment variables
Code style: Black formatting, type hints, comprehensive docstrings
Testing: Include unit tests for key components (ingestion, retrieval, query)

Constraints:

No usage of OpenAI APIs or SDKs
Stay within Qdrant Cloud Free Tier limits (collection size, upsert rate)
Stay within Neon Serverless Postgres free/compute limits
No paid external services beyond Cohere credits/API usage
Embedding dimension must match Cohere model output
Book content ingestion: Support PDF/HTML/text upload and chunking
Embedding format: Interactive widget allowing text selection with isolated RAG query

Success criteria:

Chatbot accurately answers questions using full book knowledge base
Chatbot correctly answers questions based only on user-selected text (no hallucination from outside selection)
Fast retrieval (<1s for typical queries) and relevant top-k results
Successful end-to-end demo: Ingest book → Query full book → Query selected passage
Clean repository with README, setup instructions, and .env example
No critical security vulnerabilities (e.g., proper auth if multi-user, input sanitization)
Passes all defined tests and manual verification on sample questions
Project built primarily through spec-kit-plus workflow with qwen cli for high-quality, structured output

## Response snapshot

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

## Outcome

- ✅ Impact: Created comprehensive project constitution with 6 core principles and technology requirements
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify to create feature specification based on the constitution
- 🧠 Reflection: The constitution successfully captures all project requirements and constraints in a structured format that will guide future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on this constitution
