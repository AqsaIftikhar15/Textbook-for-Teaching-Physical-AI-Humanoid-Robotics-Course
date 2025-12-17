---
description: "Task list for URL Crawl → Embed → Qdrant Upload feature implementation"
---

# Tasks: URL Crawl → Embed → Qdrant Upload

**Input**: Design documents from `/specs/001-url-crawl-embed/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend project**: `backend/` at repository root
- **Tests**: `backend/tests/`
- **Configuration**: `backend/pyproject.toml`, `backend/.env`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure
- [X] T002 Initialize Python project with uv and create pyproject.toml
- [X] T003 [P] Create .env file template with required environment variables
- [X] T004 [P] Create requirements.txt with dependencies (requests, beautifulsoup4, cohere, qdrant-client, python-dotenv)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup environment variable loading from .env file in main.py
- [X] T006 [P] Configure Cohere client with API key from environment
- [X] T007 [P] Configure Qdrant client with connection details from environment
- [X] T008 Create main.py file structure with required imports
- [X] T009 Setup basic logging configuration for the application
- [X] T010 Create utility functions for error handling and retries

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Crawl and Extract Book Content (Priority: P1) 🎯 MVP

**Goal**: System administrator runs the pipeline to crawl all Docusaurus book URLs, extract text content, and clean it for processing. The pipeline processes all pages from the book site and produces clean text chunks ready for embedding.

**Independent Test**: Can be fully tested by running the crawler against the book site and verifying that all pages are visited and text content is extracted without errors. Delivers the raw data needed for the embedding process.

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement get_all_urls function in backend/main.py to crawl book site and extract all accessible page URLs
- [X] T012 [P] [US1] Implement extract_text_from_url function in backend/main.py to extract and clean text content from a given URL
- [X] T013 [US1] Add rate limiting to URL crawling to respect target server (get_all_urls function)
- [X] T014 [US1] Implement error handling for individual URL failures in crawling process
- [ ] T015 [US1] Test URL crawling functionality with a small subset of the book site
- [ ] T016 [US1] Validate that text extraction preserves meaningful content while removing HTML tags and navigation elements

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Generate Embeddings for Content Chunks (Priority: P2)

**Goal**: System processes the extracted text chunks using Cohere embedding models to generate vector representations. The embeddings accurately represent the semantic meaning of the text chunks.

**Independent Test**: Can be fully tested by providing text chunks as input and verifying that valid embeddings are generated with appropriate dimensions and semantic coherence.

### Implementation for User Story 2

- [X] T017 [P] [US2] Implement chunk_text function in backend/main.py to split text into appropriately sized segments for embedding
- [X] T018 [P] [US2] Implement embed function in backend/main.py to generate embeddings using Cohere models for text chunks
- [X] T019 [US2] Add retry logic and rate limiting handling to the embed function
- [ ] T020 [US2] Test embedding generation with sample text chunks
- [ ] T021 [US2] Validate that generated embeddings have consistent dimensionality and represent semantic meaning

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Store Vectors in Qdrant Collection (Priority: P3)

**Goal**: System creates a Qdrant collection and stores the generated embeddings along with metadata about the source content. The storage is properly configured and accessible.

**Independent Test**: Can be fully tested by verifying that vectors and metadata are properly stored in Qdrant and can be retrieved.

### Implementation for User Story 3

- [X] T022 [P] [US3] Implement create_collection function in backend/main.py to create Qdrant collection named 'rag_embedding'
- [X] T023 [P] [US3] Implement save_chunk_to_qdrant function in backend/main.py to store embeddings with metadata in Qdrant
- [X] T024 [US3] Add proper metadata structure to Qdrant records (source URL, title, content, chunk index)
- [ ] T025 [US3] Test Qdrant storage with sample embeddings and verify retrieval
- [ ] T026 [US3] Validate that all vectors and metadata are successfully stored in Qdrant collection

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Validate Storage with Test Script (Priority: P4)

**Goal**: System provides a test script that validates the storage process by checking that vectors were properly stored and can be retrieved. The validation confirms the pipeline completed successfully.

**Independent Test**: Can be fully tested by running the validation script and confirming that stored vectors match the expected content.

### Implementation for User Story 4

- [X] T027 [P] [US4] Create validation function in backend/main.py to test storage integrity
- [X] T028 [P] [US4] Implement retrieve_and_validate function to fetch stored vectors and verify content
- [ ] T029 [US4] Add validation to confirm successful storage and report any issues
- [ ] T030 [US4] Create test script to validate the entire pipeline execution
- [ ] T031 [US4] Test validation script with various scenarios to ensure comprehensive coverage

**Checkpoint**: Complete pipeline from crawling to validation is functional

---

## Phase 7: Main Pipeline Integration

**Goal**: Integrate all components into a single main function that executes the complete pipeline

### Implementation for Main Pipeline

- [X] T032 [P] Create main function in backend/main.py to orchestrate the complete pipeline
- [X] T033 [P] Implement proper sequencing: crawl → extract → chunk → embed → store → validate
- [X] T034 Add progress tracking and status reporting to main function
- [X] T035 Add configuration parameters (chunk size, overlap, rate limits) to main function
- [X] T036 Test complete pipeline execution from start to finish

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T037 [P] Add comprehensive error logging and debugging information throughout main.py
- [X] T038 Add input validation and type checking to all functions
- [X] T039 Performance optimization for large-scale processing
- [X] T040 [P] Create test file in backend/tests/test_main.py for unit tests
- [X] T041 Security validation for API key handling
- [X] T042 Run quickstart.md validation to ensure complete functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Main Pipeline Integration (Phase 7)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for text chunks
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 for embeddings
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US3 for stored data

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority
- Main pipeline integration requires all user stories to be complete

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members
- Models and services within a story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement get_all_urls function in backend/main.py to crawl book site and extract all accessible page URLs"
Task: "Implement extract_text_from_url function in backend/main.py to extract and clean text content from a given URL"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add Main Pipeline Integration → Complete pipeline
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence