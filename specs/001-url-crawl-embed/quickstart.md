# Quickstart: URL Crawl → Embed → Qdrant Upload

## Prerequisites

- Python 3.11+
- UV package manager
- Qdrant Cloud account with API key
- Cohere API key

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Physical-AI-Robotics-Book
   ```

2. **Create and navigate to backend directory**
   ```bash
   mkdir backend
   cd backend
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
   ```

4. **Create .env file with your credentials**
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Installation

1. **Install project dependencies using UV:**
   ```bash
   uv sync
   ```

2. **Create requirements.txt (if needed):**
   ```bash
   uv pip export -o requirements.txt
   ```

## Usage

1. **Run the main pipeline:**
   ```bash
   cd backend
   python main.py
   ```

2. **The pipeline will execute in this order:**
   - Crawl all URLs from the Docusaurus book site
   - Extract and clean text from each page
   - Chunk the text into appropriate sizes
   - Generate embeddings using Cohere
   - Create Qdrant collection named 'rag_embedding'
   - Store embeddings with metadata in Qdrant

## Configuration

- **Base URL**: The pipeline targets `https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/`
- **Collection Name**: `rag_embedding` (created automatically)
- **Chunk Size**: Configurable text chunk size (default: 1024 characters)
- **Rate Limiting**: Built-in delays to be respectful to the target server

## Environment Variables

Create a `.env` file in the backend directory with:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cloud_endpoint
QDRANT_API_KEY=your_qdrant_api_key
BOOK_BASE_URL=https://aqsaiftikhar15.github.io/Textbook-for-Teaching-Physical-AI-Humanoid-Robotics-Course/
CHUNK_SIZE=1024
CHUNK_OVERLAP=100
```

## Troubleshooting

1. **API Key Issues**:
   - Verify all API keys are correctly set in `.env`
   - Check that `.env` file is in the correct directory
   - Ensure no extra spaces or quotes around the keys

2. **Connection Issues**:
   - Verify Qdrant URL is accessible
   - Check network connectivity to target book site
   - Ensure rate limiting is not blocking requests

3. **Embedding Issues**:
   - Verify Cohere API is responding
   - Check that text chunks are within size limits
   - Ensure proper text cleaning is happening

## Next Steps

1. After successful execution, the Qdrant collection will contain all embedded text chunks
2. Verify data was stored correctly using Qdrant dashboard
3. Plan retrieval functionality for the next phase