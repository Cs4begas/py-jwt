from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from model.login_request import LoginRequest
from model.login_response import LoginResponse
from service.jwt import JwtService
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["login"],
    responses={404: {"description": "Not found"}})
jwtService = JwtService()


@router.post("/login", response_model=None)
async def login(login_request: LoginRequest):
    return jwtService.login_access_refresh({"user_id": login_request.user})