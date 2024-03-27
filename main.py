from fastapi import FastAPI
from settings import Settings
from routers import login
import uvicorn



settings = Settings.ACCESS_TOKEN_EXPIRE_MINUTE
app = FastAPI()

app.include_router(login.router)

if __name__ == "__main__":
    # Start the server on 127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)