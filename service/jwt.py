from datetime import datetime, timedelta, timezone
import json
from dotenv import load_dotenv
from jose import jwt
import pytz
from db.token_repo import TokenRepo
from model.login_response import LoginResponse
from model.token import Token
from settings import Settings
import uuid


class JwtService:
    def __init__(self) -> None:
        self.token_repo = TokenRepo()

    def create_access_token(self,data: dict):
        to_encode = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=float(Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": int(expire.timestamp()), "isa": int(now.timestamp())})
        encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return encoded_jwt, expire


    def create_refresh_token(self,data: dict, count_jti_today:int) :
        to_encode = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=float(Settings.REFRESH_TOKEN_EXPIRE_MINUTES))
        nbf = now + timedelta(minutes=float(Settings.NOT_BEFORE_REFRESH_TOKEN_MINUTES))
        uuid_gen = uuid.uuid4().hex
        uuid_gen = uuid_gen + f'.{count_jti_today+1}'
        to_encode = {"jti": uuid_gen, "exp": int(expire.timestamp()), "isa": int(now.timestamp()), "nbf": int(nbf.timestamp())}
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_REFRESH_SECRET_KEY, Settings.ALGORITHM)
        return encoded_jwt, expire
    
    def login_access_refresh(self, data: dict):
        user_id = data["user_id"]
        count_jti_today = self.token_repo.count_user_token_current_date(user_id)
        access_token, expired_acess_token = self.create_access_token(data)
        refresh_token, expired_refresh_token = self.create_refresh_token(data, count_jti_today)
        token:Token = Token(access_token=access_token, refresh_token=refresh_token, user_id=user_id, expired_access_token=expired_acess_token,expired_refresh_token=expired_refresh_token , created_at= datetime.now())
        self.token_repo.insert_token(token)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)