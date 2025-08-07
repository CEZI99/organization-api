from fastapi import Header, HTTPException, status
from app.config import settings
from fastapi.security import APIKeyHeader
from fastapi import Depends


api_key_header = APIKeyHeader(name="X-API-Key", description="API Key for authentication")

async def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return x_api_key
