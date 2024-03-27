from fastapi import APIRouter

from model.login_request import LoginRequest
from service.jwt import JwtService

router = APIRouter(
    tags=["login"],
    responses={404: {"description": "Not found"}})
jwtService = JwtService()


@router.post("/login", response_model=None)
async def login(login_request: LoginRequest):
    jwtService.create_access_token({"user_id": login_request.user})