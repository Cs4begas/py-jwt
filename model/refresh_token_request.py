from attr import dataclass
from pydantic import BaseModel


@dataclass
class RefreshTokenRequest(BaseModel):
    token : str