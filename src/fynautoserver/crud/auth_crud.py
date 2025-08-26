from passlib.context import CryptContext
from fynautoserver.config.config import settings
import jwt
from datetime import datetime, timedelta
from fynautoserver.utils.index import create_response

#configs for token creation
SECRET = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGO
ACCESS_TOKEN_EXPIRY_MIN = 15
REFRESH_TOKEN_EXPIRY_DAYS = 1

# Set up context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hash the password
def hash_passsword(password:str):
    return pwd_context.hash(password)

#verify password
def verify_password(plainPassword:str,hashedPassword:str):
    return pwd_context.verify(plainPassword,hashedPassword)

#create access token
def create_Access_token(data:dict, expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN))
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)
    return encoded_jwt

#create refresh token
def create_refresh_token(data:dict):
    to_encode = data.copy()
    exipre = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    to_encode.update({'exp':exipre})
    return jwt.encode(to_encode,SECRET,algorithm=ALGORITHM)

#decode tokens
def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return create_response(success=False, result='Token expired', status_code=401)