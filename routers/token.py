from fastapi import APIRouter, HTTPException

from model.refresh_token_request import RefreshTokenRequest

router = APIRouter()


@router.post("/token/refresh")
async def getRefreshToken(refresh_token_request : RefreshTokenRequest):
    if not refresh_token_request.token:
        raise HTTPException(status_code=400, detail="Invalid request")
