from datetime import datetime
from pydantic import BaseModel

class Token(BaseModel):
    access_token : str
    refresh_token: str
    user_id: str
    expired_access_token: datetime
    expired_refresh_token: datetime
    created_at: datetime