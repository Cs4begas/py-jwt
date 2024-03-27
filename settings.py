from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

class Settings:
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTE = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTE')
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PWD = os.getenv('DB_PWD')
    DB_USR = os.getenv('DB_USR')
        

    