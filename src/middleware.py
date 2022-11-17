from config import ACCESS_SECRET, TOKEN_NAME
from fastapi import HTTPException, Request
from src.utils import token_is_valid


async def process_resource(request:Request):
    token = request.headers.raw
    for head in token:
        if head[0] == b'authorization':
            token = str(head[1])[2:-1]
            break
    if not token:
        raise HTTPException(401,
                            "Auth token required, Please provide an auth token as part of the request.",
                            )
    token_data = await token_is_valid(token, ACCESS_SECRET)
    if not token_data:
        raise HTTPException(401,
                            "Authentication required, Token not valid or expired"
                            )
    return token_data
