from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
#SECRET_KEY
#ALGO
#EXPIRATION_TIME

OAuth2_schema = OAuth2PasswordBearer(tokenUrl="login") # get the token from this URL

SECRET_KEY = settings.secret_key
ALGORITHM= settings.algorithm
EXPIRATION_TIME = settings.access_token_expire_mins

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp": expire}) #
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check token expiration
        expire_time = decoded_token.get("exp")
        if expire_time is None or datetime.utcfromtimestamp(expire_time) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired"
            )
        #while creating the token the data we entered
        #access_token = oauth2.create_access_token(data={"borrower_id": borrower.borrower_id})
        borrower_id = decoded_token.get("borrower_id")
        if not borrower_id:
            raise credential_exception

        token_data = schemas.TokenData(id=borrower_id)
    except JWTError:
        raise credential_exception

    return token_data
    
def get_current_borrower(token:str = Depends(OAuth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate credentials',
                                         headers={'WWWW-Authenticate':"Bearer"})
    return verify_access_token(token, credential_exception)