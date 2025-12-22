# Feature Specification: Integrated RAG Chatbot

**Feature Branch**: `001-integrated-rag-chatbot`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Integrated RAG Chatbot Embedded in Published Book Target deliverable: A fully functional, high-quality Retrieval-Augmented Generation (RAG) chatbot,using speckitplus for projectscaffolding, embedded within a published digital book, capable of answering user questions based on the entire book content or strictly limited to user-selected text passages. Core functionality focus: Ingest and index the full book content (PDF/text/HTML) into a persistent vector database Support two distinct query modes: Full-book mode: Answer questions using knowledge from the entire book Selected-text mode: Answer questions using ONLY the user-highlighted/selected passage (no external knowledge or full-book bleed) Deliver responses that are accurate, concise, well-grounded, and faithful to the source material Interactive embedding: Chatbot widget integrated directly into the book viewer with text selection triggering isolated queries Success criteria: End-to-end pipeline works: Upload book → Auto-ingest and chunk → Embed with Cohere → Store in Qdrant → Query via FastAPI backend → Accurate responses from Cohere generation Full-book queries return relevant, cited, non-hallucinated answers with high faithfulness to book content Selected-text queries respond exclusively based on the provided passage (verified by testing questions that would require full-book knowledge otherwise) Response latency < 2 seconds for typical queries on free-tier infrastructure Clean, production-ready codebase with full setup instructions, environment configuration, and basic tests Secure handling of API keys and database connections Successful demo on a sample book (e.g., public domain or personal test book) Technical stack (must use): LLM provider: Cohere only (API key provided) Embedding model: Cohere embed-english-v3.0 or embed-multilingual-v3.0 Generation model: Cohere Command R, R+, or latest Command series Vector database: Qdrant Cloud Free Tier (using provided URL and API key) Metadata/relational storage: Neon Serverless Postgres (using provided connection URL) Backend: FastAPI (async, proper routing, error handling) Ingestion: Support PDF/text ingestion with intelligent chunking (semantic/overlapping) Secrets: All credentials loaded via environment variables (exact values below to be used in development) Required credentials (use exactly these) Constraints: No usage of OpenAI APIs, SDKs, or models at any point Must stay within free-tier limits of Qdrant Cloud and Neon Serverless Postgres and Cohere Trial API No additional paid services beyond the free tiers specified Code must be Python-based, cleanly structured, type-hinted, and well-documented Project built through spec-kit-plus workflow using qwen cli for iterative refinement chatbot must work in web-based book formats(e.g, HTML/JS embed) and support mobile responsiveness Not building: Multi-user authentication or persistent chat history across sessions Advanced UI/frontend beyond basic functional embedding (focus on backend RAG pipeline) Real-time collaborative editing or live book updates Mobile app or separate deployment platform (focus on embeddable widget/backend) Extensive error recovery or monitoring dashboard Support for images, tables, or multimodal content in the book (text-only RAG) full scale production deployment beyond free tiers"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Query Full Book Content (Priority: P1)

A book reader wants to ask a question about the book they're reading and receive accurate, relevant answers based on the entire book content. They interact with an embedded chatbot widget within the digital book interface, type their question, and receive a response grounded in the book's content without any hallucinations.

**Why this priority**: This is the foundational functionality that makes the chatbot useful - allowing users to interact with the entire book content for comprehensive understanding.

**Independent Test**: Can be fully tested by uploading a sample book, ingesting its content, and asking broad questions about the book to verify the system returns accurate answers based on the full book content.

**Acceptance Scenarios**:

1. **Given** a book has been successfully ingested and indexed, **When** a user asks a question about the book content, **Then** the system returns a relevant, accurate answer based on the entire book content.
2. **Given** a user is reading a digital book with the embedded chatbot, **When** they submit a question, **Then** the response is generated within 2 seconds with citations to the relevant book content.
3. **Given** a user asks a question requiring comprehensive understanding of the book, **When** the system processes the query, **Then** the response demonstrates knowledge from multiple parts of the book.

---

### User Story 2 - Query Selected Text Only (Priority: P2)

A book reader has selected specific text in the book and wants to ask questions only about that selected passage, without the system drawing from other parts of the book. The chatbot must respond exclusively based on the provided text selection.

**Why this priority**: This feature enables focused, detailed discussions about specific sections of the book, which is valuable for studying and comprehension.

**Independent Test**: Can be tested by selecting text passages and asking questions that would require full-book knowledge if answered correctly, verifying the system responds only based on the selected text.

**Acceptance Scenarios**:

1. **Given** a user has selected specific text in the book, **When** they ask a question related to that text, **Then** the system responds based only on the selected text without referencing other parts of the book.
2. **Given** a user asks a question that requires knowledge outside the selected text, **When** they submit the query, **Then** the system acknowledges the limited scope and answers only what can be inferred from the selected text.
3. **Given** a user selects text and triggers the chatbot, **When** they ask a question, **Then** the response is generated within 2 seconds and is strictly grounded in the selected text.

---

### User Story 3 - Book Ingestion and Indexing (Priority: P2)

A content administrator needs to upload a book in PDF, text, or HTML format to the system, and have it automatically processed, chunked, embedded, and indexed into the vector database for retrieval.

**Why this priority**: Without this functionality, the other user stories cannot work, making it essential for the overall system operation.

**Independent Test**: Can be tested by uploading different book formats and verifying the content is properly ingested, chunked, embedded, and stored in the vector database.

**Acceptance Scenarios**:

1. **Given** a PDF, text, or HTML book file, **When** it is uploaded to the system, **Then** the content is successfully ingested and indexed for RAG queries.
2. **Given** a book is being ingested, **When** the process runs, **Then** the text is properly chunked using semantic or overlapping strategies for optimal retrieval quality.
3. **Given** a book has been ingested, **When** a query is made, **Then** the system can retrieve relevant content from the indexed book.

---

### Edge Cases

- What happens when a user asks a question that cannot be answered based on the book content?
- How does the system handle very long text selections in selected-text mode?
- What happens when a book contains both text and images, but only text can be processed?
- How does the system handle books with multiple languages?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support ingestion of PDF, text, and HTML book formats
- **FR-002**: System MUST process book content into semantic or overlapping chunks for optimal retrieval quality
- **FR-003**: Users MUST be able to ask questions about the full book content and receive accurate, non-hallucinated responses
- **FR-004**: System MUST support selected-text query mode that responds only based on user-selected text passages
- **FR-005**: System MUST generate responses with less than 2 seconds latency for typical queries
- **FR-006**: System MUST store embeddings in Qdrant vector database with metadata linking to Neon Postgres if needed
- **FR-007**: Users MUST be able to see citations or references to the relevant book content in chatbot responses
- **FR-008**: System MUST handle API keys and database connections securely through environment variables
- **FR-009**: System MUST support embedding model Cohere embed-english-v3.0 or embed-multilingual-v3.0
- **FR-010**: System MUST use Cohere Command R or R+ for response generation

### Key Entities

- **Embedded Chatbot**: Interactive widget integrated into the book viewer that processes user questions and returns relevant responses
- **Book Content**: The text content of the published digital book that serves as the knowledge base for the RAG system
- **User Queries**: Questions posed by users about the book content, either in full-book mode or selected-text mode
- **Response**: Generated answers that are accurate, concise, well-grounded, and faithful to the source material

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: End-to-end pipeline works: Upload book → Auto-ingest and chunk → Embed with Cohere → Store in Qdrant → Query via FastAPI backend → Accurate responses from Cohere generation
- **SC-002**: Full-book queries return relevant, cited, non-hallucinated answers with high faithfulness to book content as verified by manual testing with sample questions
- **SC-003**: Selected-text queries respond exclusively based on the provided passage (verified by testing questions that would require full-book knowledge otherwise)
- **SC-004**: Response latency is less than 2 seconds for typical queries on free-tier infrastructure
- **SC-005**: System successfully processes and responds to queries for at least 3 different books in different formats (PDF, text, HTML)
- **SC-006**: All API keys and sensitive credentials are handled securely without being exposed in code or logs