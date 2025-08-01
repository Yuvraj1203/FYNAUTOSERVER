from fastapi import Request, status, HTTPException
from fynautoserver.utils.index import create_response
from fynautoserver.crud.auth_crud import decode_access_token
import jwt

def get_current_user(request:Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Unauthorized"
        )
    
    token = auth_header.split(" ")[1]

    try:
        payload = decode_access_token(token)
        print(payload,"==================================================")
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )