from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
from .routes import ingest, query, monitor
from .middleware.auth import api_key_auth
import traceback
import logging
from fastapi import Security, Depends, HTTPException
from fastapi.security import APIKeyHeader
from src.config.settings import settings

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Integrated RAG Chatbot API",
    description="A RAG chatbot that can answer questions based on full book content or selected text passages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
#app.middleware("http")(api_key_auth)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        if not api_key.startswith("Bearer ") or api_key[7:] != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return api_key

# Include routes
app.include_router(ingest.router, prefix="/ingest", tags=["ingestion"], dependencies=[Depends(get_api_key)])
app.include_router(query.router, prefix="/query", tags=["query"], dependencies=[Depends(get_api_key)])
app.include_router(monitor.router, prefix="/monitor", tags=["monitoring"], dependencies=[Depends(get_api_key)])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}\nTraceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "traceback": traceback.format_exc().splitlines()
        }
    )

@app.get("/")
async def root():
    return {"message": "Integrated RAG Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}