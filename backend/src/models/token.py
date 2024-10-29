from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    expires_at: datetime
