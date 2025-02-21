from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError 
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from Models.model import Signup
from config.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, User_details
from typing import Dict


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def decode_token(token: str) -> Signup:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if token is None:
        return None

    token = token.removeprefix("Bearer").strip()  
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("email")
       
        if username is None:
            raise credentials_exception
        user = get_user(username)
        
        return user
    except JWTError as e:
       
        raise credentials_exception
    
def get_user(email:str):
    
    Existing_user= User_details.find_one({'email': email})
    if not  Existing_user:
        return None
    else:
        return Existing_user
