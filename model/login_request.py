from attr import dataclass
from pydantic import BaseModel


@dataclass
class LoginRequest(BaseModel):
    user : str
    password: str