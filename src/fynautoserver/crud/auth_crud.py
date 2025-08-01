from passlib.context import CryptContext
from fynautoserver.config.config import settings
import jwt
from datetime import datetime, timedelta

#configs for token creation
SECRET = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGO
ACCESS_TOKEN_EXPIRY_MIN = 30

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

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET,algorithms=ALGORITHM)
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None