# Tasks: Integrated RAG Chatbot

## Implementation Strategy

This tasks document implements the Integrated RAG Chatbot feature following the spec-driven development approach. The implementation proceeds in phases with user stories as milestones:

- **MVP Scope**: User Story 3 (Book Ingestion) and User Story 1 (Full Book Query) as minimal viable functionality
- **Incremental Delivery**: Each user story builds upon the previous to create a complete, testable system
- **Parallel Execution**: Tasks marked [P] can be executed in parallel when they involve different files/components
- **Independent Testing**: Each user story has clear test criteria for verification

## Dependencies

- **User Story 3 (P2)** must be completed before **User Story 1 (P1)** since the full-book query requires an ingested book
- **User Story 3 (P2)** should also be completed before **User Story 2 (P2)** since selected-text queries may benefit from ingested book metadata

## Parallel Execution Examples

- All model creation tasks can run in parallel [P]
- All service implementation tasks can run in parallel after models are defined [P]
- API route development can run in parallel after services are implemented [P]

---

## Phase 1: Setup & Environment

- [X] T001 Create project directory structure per implementation plan in backend_backup/
- [X] T002 Create requirements.txt with dependencies: cohere, qdrant-client, psycopg2/asyncpg, fastapi, uvicorn, pydantic, python-dotenv, PyMuPDF, beautifulsoup4
- [X] T003 Create .env.example with required credentials from spec
- [X] T004 Create .gitignore with proper Python/IDE ignores
- [X] T005 Set up FastAPI application in backend_backup/src/api/main.py
- [X] T006 Create configuration module in backend_backup/src/config/settings.py with environment loading

## Phase 2: Foundational Components

- [X] T007 Create Book model in backend_backup/src/models/book.py with all required fields from data model
- [X] T008 Create Chunk model in backend_backup/src/models/chunk.py with all required fields from data model
- [X] T009 Create Query model in backend_backup/src/models/query.py with all required fields from data model
- [X] T010 Create embedding service in backend_backup/src/services/embedding.py for Cohere integration
- [X] T011 Create storage service in backend_backup/src/services/storage.py for Qdrant and Neon Postgres interaction
- [X] T012 Create ingestion service in backend_backup/src/services/ingestion.py for PDF/HTML/text processing
- [X] T013 Create authentication middleware in backend_backup/src/api/middleware/auth.py with API key validation

## Phase 3: User Story 3 - Book Ingestion and Indexing (Priority: P2)

**Goal**: Enable content administrator to upload PDF, text, or HTML book format and have it automatically processed, chunked, embedded, and indexed

**Independent Test**: Upload different book formats and verify the content is properly ingested, chunked, embedded, and stored in the vector database.

**Acceptance**:
1. PDF, text, or HTML book file is uploaded to the system
2. Content is successfully ingested and indexed for RAG queries
3. Text is properly chunked using semantic or overlapping strategies for optimal retrieval quality
4. After ingestion, system can retrieve relevant content from the indexed book

- [X] T014 [US3] Create Book ingestion schema in backend_backup/src/models/book.py with Pydantic validation
- [X] T015 [P] [US3] Implement PDF text extraction in backend_backup/src/services/ingestion.py
- [X] T016 [P] [US3] Implement HTML text extraction in backend_backup/src/services/ingestion.py
- [X] T017 [P] [US3] Implement TEXT file processing in backend_backup/src/services/ingestion.py
- [X] T018 [P] [US3] Create semantic chunking algorithm in backend_backup/src/services/ingestion.py
- [X] T019 [P] [US3] Create overlapping chunking algorithm in backend_backup/src/services/ingestion.py
- [X] T020 [P] [US3] Implement text preprocessing (cleaning, normalization) in backend_backup/src/services/ingestion.py
- [X] T021 [P] [US3] Implement file validation for upload in backend_backup/src/api/routes/ingest.py
- [X] T022 [US3] Create ingestion endpoint POST /ingest/upload in backend_backup/src/api/routes/ingest.py
- [X] T023 [US3] Implement book status tracking (PROCESSING, READY, ERROR) in backend_backup/src/services/ingestion.py
- [X] T024 [US3] Create status endpoint GET /ingest/status/{book_id} in backend_backup/src/api/routes/ingest.py
- [X] T025 [P] [US3] Connect embedding service to generate embeddings for chunks in backend_backup/src/services/ingestion.py
- [X] T026 [P] [US3] Connect storage service to store embeddings in Qdrant in backend_backup/src/services/ingestion.py
- [X] T027 [P] [US3] Connect storage service to store metadata in Neon Postgres in backend_backup/src/services/ingestion.py
- [X] T028 [P] [US3] Implement async processing for large files in backend_backup/src/services/ingestion.py
- [X] T029 [US3] Implement ingestion progress tracking in backend_backup/src/services/ingestion.py

## Phase 4: User Story 1 - Query Full Book Content (Priority: P1)

**Goal**: Allow book reader to ask questions about the book and receive accurate, relevant answers based on entire book content

**Independent Test**: Upload a sample book, ingest its content, and ask broad questions about the book to verify system returns accurate answers based on the full book content.

**Acceptance**:
1. Book is successfully ingested and indexed
2. User asks a question about the book content and receives relevant, accurate answer based on entire book
3. Response generated within 2 seconds with citations to relevant book content
4. Response demonstrates knowledge from multiple parts of the book for questions requiring comprehensive understanding

- [X] T030 [US1] Create full-book query schema in backend_backup/src/models/query.py with Pydantic validation
- [X] T031 [US1] Implement vector search in storage service backend_backup/src/services/storage.py to retrieve relevant chunks
- [X] T032 [P] [US1] Implement RAG orchestration service in backend_backup/src/services/rag.py for full-book queries
- [X] T033 [P] [US1] Create Cohere generation integration for full-book queries in backend_backup/src/services/rag.py
- [X] T034 [P] [US1] Implement response formatting with citations in backend_backup/src/services/rag.py
- [X] T035 [P] [US1] Create query history tracking in backend_backup/src/services/rag.py
- [X] T036 [US1] Create full-book query endpoint POST /query/full in backend_backup/src/api/routes/query.py
- [X] T037 [US1] Implement response time tracking in backend_backup/src/services/rag.py
- [X] T038 [US1] Implement token usage tracking in backend_backup/src/services/rag.py
- [X] T039 [US1] Implement query validation to ensure book exists and is ready in backend_backup/src/api/routes/query.py
- [X] T040 [US1] Add performance optimization to ensure <2s response time in backend_backup/src/services/rag.py

## Phase 5: User Story 2 - Query Selected Text Only (Priority: P2)

**Goal**: Allow book reader to select specific text and ask questions only about that passage, with system responding exclusively based on the provided text

**Independent Test**: Select text passages and ask questions that would require full-book knowledge if answered correctly, verifying system responds only based on the selected text.

**Acceptance**:
1. User selects specific text in the book and asks related question
2. System responds based only on the selected text without referencing other parts of the book
3. For questions requiring knowledge outside selected text, system acknowledges limited scope and answers what can be inferred from selected text
4. Response generated within 2 seconds and strictly grounded in selected text

- [X] T041 [US2] Create selected-text query schema in backend_backup/src/models/query.py with Pydantic validation
- [X] T042 [US2] Implement selected-text generation service in backend_backup/src/services/rag.py
- [X] T043 [US2] Create selected-text query endpoint POST /query/selected in backend_backup/src/api/routes/query.py
- [X] T044 [US2] Implement strict isolation to prevent knowledge bleed in backend_backup/src/services/rag.py
- [X] T045 [US2] Add validation to ensure selected text is not empty in backend_backup/src/api/routes/query.py
- [X] T046 [US2] Implement response formatting without citations in backend_backup/src/services/rag.py (since no vector search is used)
- [X] T047 [US2] Add performance optimization for selected-text mode in backend_backup/src/services/rag.py

## Phase 6: Monitoring & Usage Tracking

- [X] T048 Create usage monitoring script in backend_backup/scripts/monitor_usage.py
- [X] T049 Create monitoring endpoint GET /monitor/usage in backend_backup/src/api/routes/monitor.py
- [X] T050 Create system health endpoint GET /monitor/status in backend_backup/src/api/routes/monitor.py
- [X] T051 Implement Qdrant usage tracking in backend_backup/scripts/monitor_usage.py
- [X] T052 Implement Neon Postgres usage tracking in backend_backup/scripts/monitor_usage.py
- [X] T053 Add usage alerting when approaching limits in backend_backup/scripts/monitor_usage.py

## Phase 7: Testing & Verification

- [X] T054 Write unit tests for ingestion service backend_backup/tests/unit/test_ingestion.py
- [X] T055 Write unit tests for embedding service backend_backup/tests/unit/test_embedding.py
- [X] T056 Write unit tests for storage service backend_backup/tests/unit/test_storage.py
- [X] T057 Write unit tests for RAG service backend_backup/tests/unit/test_rag.py
- [X] T058 Write integration tests for full-book query flow backend_backup/tests/integration/test_full_book_query.py
- [X] T059 Write integration tests for selected-text query flow backend_backup/tests/integration/test_selected_text_query.py
- [X] T060 Write integration tests for ingestion flow backend_backup/tests/integration/test_ingestion.py
- [X] T061 Write contract tests for API endpoints backend_backup/tests/contract/test_api_contracts.py
- [X] T062 Implement response accuracy verification tests backend_backup/tests/unit/test_response_accuracy.py
- [X] T063 Create test dataset with sample books backend_backup/tests/data/

## Phase 8: Documentation & Demo Preparation

- [X] T064 Create comprehensive README.md with setup instructions
- [X] T065 Prepare sample book for demo in backend_backup/demo/
- [X] T066 Create API documentation with usage examples
- [X] T067 Document deployment instructions for different environments
- [X] T068 Create troubleshooting guide for common issues

## Phase 9: Polish & Cross-Cutting Concerns

- [ ] T069 Add comprehensive error handling throughout the application
- [ ] T070 Add detailed logging for debugging and monitoring
- [ ] T071 Add proper exception handling and user-friendly messages
- [ ] T072 Optimize performance based on testing results
- [ ] T073 Review and enhance security measures
- [ ] T074 Conduct final system testing with sample books
- [ ] T075 Prepare final documentation and code cleanup