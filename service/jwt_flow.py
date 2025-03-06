from http import HTTPStatus
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import ExpiredSignatureError, JWTError, jwt
import pytz
from db.redis_manager import RedisManager
from db.token_repo import TokenRepo
from model.login_response import LoginResponse
from settings import Settings
from model.token import Token
import uuid


class JwtService:
    def __init__(self) -> None:
        self.token_repo = TokenRepo()
        self.redis = RedisManager()

    def __create_access_token(self,data: dict):
        to_encode = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=float(Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": int(expire.timestamp()), "iat": int(now.timestamp())})
        encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return encoded_jwt, expire

    def __create_refresh_token(self,data: dict, count_jti_today:int) :
        to_encode = data.copy()
        now = datetime.now()
        expire = now + timedelta(minutes=float(Settings.REFRESH_TOKEN_EXPIRE_MINUTES))
        nbf = now + timedelta(minutes=float(Settings.NOT_BEFORE_REFRESH_TOKEN_MINUTES))
        uuid_gen = uuid.uuid4().hex
        uuid_gen = uuid_gen + f'.{count_jti_today}'
        to_encode.update({"jti": uuid_gen, "exp": int(expire.timestamp()), "iat": int(now.timestamp()), "nbf": int(nbf.timestamp())})
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_REFRESH_SECRET_KEY, Settings.ALGORITHM)
        return encoded_jwt, expire
    
    def login_access_refresh(self, data: dict):
        user_id = data["user_id"]
        access_token, expired_acess_token = self.__create_access_token(data)
        refresh_token, expired_refresh_token = self.__create_refresh_token(data, 1)
        self.redis.redis_client.set(user_id, json.dumps({"access_token": access_token, "refresh_token": refresh_token}), ex=int(expired_refresh_token.timestamp()-datetime.now().timestamp()))
        token:Token = Token(access_token=access_token, refresh_token=refresh_token, user_id=user_id, expired_access_token=expired_acess_token,expired_refresh_token=expired_refresh_token , created_at= datetime.now())
        self.token_repo.insert_token(token)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
    
    def authenticate_access_token(self, token:str):
        try :
            self.check_blacklist(token)
            jwt.decode(token, key=Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
        except ExpiredSignatureError as es:
            print(es)
            return False
        except Exception as e:
            print(e)
            return False
        return True
    
    def request_refresh_token(self, token:str):
        now = datetime.now().timestamp()
        try :
            data = jwt.decode(token, key=Settings.JWT_REFRESH_SECRET_KEY, algorithms=Settings.ALGORITHM)
            if(self.check_blacklist(token)):
                bl_ac_token_cache, bl_refresh_token_cache = self.get_cache_token(data['user_id'])
                if(bl_ac_token_cache is None or bl_refresh_token_cache is None) :
                    return False
                self.invalidate_token(bl_ac_token_cache, bl_refresh_token_cache)
                self.redis.redis_client.delete(data['user_id'])
                return False
        except ExpiredSignatureError as es:
            print(es)
            return False
        except JWTError as e:
            print(e)
            return False
        if(int(now) <= data['nbf']):
            raise Exception("This refresh token is before the time that should refresh")
        jti:str = data['jti']
        count_jti = int(jti.split(".")[1])
        user_id = data['user_id']
        access_token, expired_acess_token = self.__create_access_token({"user_id": user_id})
        refresh_token, expired_refresh_token = self.__create_refresh_token({"user_id": user_id}, count_jti)

        bl_ac_token_cache, bl_refresh_token_cache = self.get_cache_token(user_id)
        self.redis.redis_client.set(user_id, json.dumps({"access_token": access_token, "refresh_token": refresh_token}), ex=int(expired_refresh_token.timestamp()-datetime.now().timestamp()))
        token:Token = Token(access_token=access_token, refresh_token=refresh_token, user_id=user_id, expired_access_token=expired_acess_token,expired_refresh_token=expired_refresh_token , created_at= datetime.now())
        self.token_repo.insert_token(token)

        self.invalidate_token(bl_ac_token_cache, bl_refresh_token_cache)

        return LoginResponse(access_token=access_token, refresh_token=refresh_token)
    
    def check_blacklist(self, token:str):
        bl_check = self.redis.redis_client.get(f'bl_{token}')
        if(bl_check):
           return True
        return False
        
    def invalidate_token(self, access_token:str, refresh_token:str):
        self.redis.redis_client.set(f'bl_{access_token}', access_token, ex=360)
        self.redis.redis_client.set(f'bl_{refresh_token}', refresh_token, ex=360)
    
    def get_cache_token(self, user_id):
        token_cache = self.redis.redis_client.get(user_id)
        token_cache_val = json.loads(token_cache)
        bl_ac_token_cache = token_cache_val.get('access_token')
        bl_refresh_token_cache = token_cache_val.get('refresh_token')
        return bl_ac_token_cache, bl_refresh_token_cache


