from fastapi import FastAPI
from db.db import DB
from settings import Settings
from routers import login
import uvicorn


app = FastAPI()

app.include_router(login.router)

if __name__ == "__main__":
    # Start the server on 127.0.0.1:8000
    DB()
    uvicorn.run(app, host="127.0.0.1", port=8000)