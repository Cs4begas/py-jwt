from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from urllib3 import HTTPResponse

from model.login_request import LoginRequest
from model.login_response import LoginResponse
from model.refresh_token_request import RefreshTokenRequest
from service.auth_bearer import JWTBearer
from service.jwt_flow import JwtService
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["login"],
    responses={404: {"description": "Not found"}})
jwtService = JwtService()


@router.post("/login", response_model=None)
async def login(login_request: LoginRequest):
    return jwtService.login_access_refresh({"user_id": login_request.user})

@router.get("/authen", dependencies=[Depends(JWTBearer())])
async def authen():
    print("test")
    return JSONResponse(content={"message": "authen success"}, media_type="application/json")

@router.post("/refresh-token")
async def refresh_token(refresh_token_request: RefreshTokenRequest):
    return jwtService.request_refresh_token(refresh_token_request.refresh_token)