from typing import Optional
from attr import dataclass
from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token : str
    refresh_token: Optional[str] = None