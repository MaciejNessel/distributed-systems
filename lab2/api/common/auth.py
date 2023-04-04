from fastapi import Header, HTTPException

from .config import Config


async def check_token(token: str = Header(None)):
    if token != Config.MY_API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
