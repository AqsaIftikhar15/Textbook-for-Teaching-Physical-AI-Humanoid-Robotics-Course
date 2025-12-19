import requests
from fastapi import APIRouter, HTTPException, status
from src.config.settings import settings
from datetime import datetime
import subprocess
import sys
import logging

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

@router.get("/usage")
async def get_usage():
    """
    Get current usage metrics for Qdrant Cloud and Neon Serverless Postgres
    to ensure staying within free-tier limits.
    """
    try:
        logger.info("Fetching usage metrics")

        # Qdrant usage metrics (we'll simulate these since direct metrics aren't available through the API)
        # In a real implementation, you would need to track this using your own counters
        qdrant_usage = {
            "collection_size": 15000,  # Simulated value
            "max_collection_size": 50000,  # Free tier limit
            "upsert_count": 250,  # Simulated value
            "max_upsert_per_month": 100000,  # Free tier limit
            "percentage_used": 30.0
        }

        # Neon Postgres usage metrics (we'll simulate these)
        # In a real implementation, you would need to track this using your own counters
        neon_usage = {
            "compute_time_used": 7200,  # in seconds, simulated value
            "max_compute_time": 14400,  # in seconds (4 hours) - free tier limit
            "data_transfer_used": 0.5,  # in GB, simulated value
            "max_data_transfer": 10,  # in GB - free tier limit
            "percentage_used": 50.0
        }

        # Cohere usage metrics (we'll simulate these)
        # In a real implementation, you would need to track this using your own counters
        cohere_usage = {
            "api_calls_made": 450,  # Simulated value
            "max_api_calls": 10000,  # Per month, assumed limit
            "percentage_used": 4.5
        }

        # Calculate recommendations based on usage
        recommendations = []
        if neon_usage["percentage_used"] >= 80:
            recommendations.append("Neon compute time approaching limits - consider optimizing queries")
        elif neon_usage["percentage_used"] >= 50:
            recommendations.append("Neon compute time at 50% - consider optimizing queries")

        if qdrant_usage["percentage_used"] >= 80:
            recommendations.append("Qdrant usage approaching limits - monitor closely")
        elif qdrant_usage["percentage_used"] >= 50:
            recommendations.append("Qdrant usage at 30% - within safe limits")

        usage_data = {
            "timestamp": datetime.now().isoformat(),
            "qdrant_usage": qdrant_usage,
            "neon_usage": neon_usage,
            "cohere_usage": cohere_usage,
            "recommendations": recommendations
        }

        logger.info("Usage metrics retrieved successfully")
        return usage_data
    except Exception as e:
        logger.error(f"Error retrieving usage metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving usage metrics: {str(e)}"
        )

@router.get("/status")
async def get_system_status():
    """
    Get the overall system health status.
    """
    try:
        logger.info("Checking system status")

        # Check Qdrant connection
        qdrant_status = "disconnected"
        try:
            # Attempt to connect to Qdrant
            from qdrant_client import QdrantClient
            client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
            # Try to get collections as a basic health check
            client.get_collections()
            qdrant_status = "connected"
            logger.info("Qdrant connection: OK")
        except Exception as e:
            logger.error(f"Qdrant connection failed: {str(e)}", exc_info=True)

        # Check Neon connection
        neon_status = "disconnected"
        try:
            # Test connection to Neon DB
            import psycopg2
            test_conn = psycopg2.connect(settings.neon_db_url)
            test_conn.close()
            neon_status = "connected"
            logger.info("Neon connection: OK")
        except Exception as e:
            logger.error(f"Neon connection failed: {str(e)}", exc_info=True)

        # Check Cohere API
        cohere_status = "disconnected"
        try:
            import cohere
            co = cohere.Client(settings.cohere_api_key)
            # Simple check by attempting to get embeddings with minimal text
            co.embed(texts=["test"], model="embed-english-v3.0")
            cohere_status = "connected"
            logger.info("Cohere API: OK")
        except Exception as e:
            logger.error(f"Cohere API failed: {str(e)}", exc_info=True)

        # Application status (always running if this endpoint is accessible)
        app_status = "running"

        status_data = {
            "status": "healthy" if all(s == "connected" for s in [qdrant_status, neon_status, cohere_status]) else "degraded",
            "services": {
                "qdrant_connection": qdrant_status,
                "neon_connection": neon_status,
                "cohere_api": cohere_status,
                "application": app_status
            },
            "last_updated": datetime.now().isoformat()
        }

        logger.info(f"System status check completed: {status_data['status']}")
        return status_data
    except Exception as e:
        logger.error(f"Error checking system status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking system status: {str(e)}"
        )