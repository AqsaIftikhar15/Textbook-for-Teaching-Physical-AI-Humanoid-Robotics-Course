from fastapi import Request, HTTPException, status
from src.config.settings import settings
from typing import Callable, Awaitable
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# HTTP Bearer token for API key authentication
security = HTTPBearer()

async def api_key_auth(request: Request, call_next: Callable) -> Callable:
    """
    Middleware to authenticate requests using API key
    """
    # Skip authentication for health check and root endpoints
    if request.url.path in ["/", "/health"]:
        return await call_next(request)
    
    # Get the authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    
    # Extract the token
    token = auth_header[7:]  # Remove "Bearer " prefix
    
    # Validate the token
    if token != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # Add the authenticated request to the request state
    request.state.authenticated = True
    
    response = await call_next(request)
    return response