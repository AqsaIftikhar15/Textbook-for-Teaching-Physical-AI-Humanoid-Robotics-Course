# Research: Integrated RAG Chatbot

## Decision: Cohere API Integration
- **Rationale**: The specification requires using Cohere exclusively, specifically embed-english-v3.0 or embed-multilingual-v3.0 for embeddings and Command R, R+, or latest Command series for generation. These models provide good balance of accuracy, multilingual support, and cost-effectiveness.
- **Alternatives considered**: OpenAI models (not allowed per constraints), other embedding models like Sentence Transformers (not allowed per constraints).

## Decision: PDF/HTML/Text Processing
- **Rationale**: PyMuPDF (fitz) provides robust PDF text extraction with good handling of various PDF formats, while beautifulsoup4 offers reliable HTML parsing. These libraries are commonly used in production systems for document processing.
- **Alternatives considered**: PyPDF2 (limited in handling complex PDFs), pdfplumber (more specialized), lxml (more complex for basic HTML parsing).

## Decision: Chunking Strategy
- **Rationale**: Semantic chunking with overlap maintains context while allowing effective retrieval. This approach splits content by meaning rather than fixed character/word counts, leading to better retrieval quality.
- **Alternatives considered**: Fixed-size chunking (can split context), sentence-based chunking (may not optimize for meaning).

## Decision: Qdrant Vector Storage
- **Rationale**: Required by specification to use Qdrant Cloud Free Tier. It supports rich metadata storage alongside vectors, which is essential for linking to Postgres metadata. It's also well-documented and performant.
- **Alternatives considered**: Pinecone, Weaviate, Milvus (not allowed per constraints).

## Decision: Backend Framework
- **Rationale**: FastAPI was specified as required technology. It provides async support, automatic API documentation (Swagger), and excellent performance for API services.
- **Alternatives considered**: Flask, Django (not allowed per constraints).

## Decision: Database for Metadata
- **Rationale**: Neon Serverless Postgres was specified as required technology. It provides serverless PostgreSQL with excellent integration possibilities and is cost-effective.
- **Alternatives considered**: Various other databases (not allowed per constraints).

## Decision: Monitoring Approach
- **Rationale**: Implement a separate monitoring script to track usage of Qdrant Cloud and Neon Serverless Postgres against free-tier limits. This ensures we stay within allowed usage.
- **Alternatives considered**: Built-in monitoring vs custom scripts (custom scripts provide more control).