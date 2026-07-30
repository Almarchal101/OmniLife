from ulid import ULID
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from core.config import settings
import jwt
import uuid
password_hash = PasswordHash.recommended()
from fastapi import HTTPException, status


#genererar en unik id med 32 bitar hexal som används som id for user och andra element 
def generate_ulid() -> str:
    return str(ULID())

#genererar en hashed?password
def get_password_hashed(password):
    return password_hash.hash(password)

#varifererar arr en password är rätt
def verify_password(plain_password, hash_password):
    return password_hash.verify(plain_password, hash_password)



def _create_token(user_data: dict, expires_delta: timedelta, token_type: str):
    
    to_encode = user_data.copy()
    now = datetime.now(timezone.utc)
    
    to_encode.update({
          
          'exp': now + expires_delta,
          'iat': now,
          'jti': str(uuid.uuid4()),
          'token_type': token_type,
        
        })
    
    encode_jwt = jwt.encode(to_encode, settings.jwt_secret_key.get_secret_value(), algorithm = settings.jwt_algorithm)
    
    return encode_jwt


def create_access_token(user_id: str) -> str:
    return _create_token({
        "sub": str(user_id)
    },
        expires_delta =  timedelta(minutes = settings.access_token_expire_minutes),
        token_type = "access_token"   
    )
    

def create_refresh_token(user_id: str) -> str:
    return _create_token({
        "sub": str(user_id)
    },
        expires_delta =  timedelta(days = settings.refresh_token_expire_days),
        token_type = "refresh_token"   
    )
    
    
def decode_token(token: str, expected_type: str = None) -> dict:
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key.get_secret_value(), 
            algorithms=[settings.jwt_algorithm]
        )
        
        if expected_type and payload.get("token_type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
            
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "token has expierd"
            
        )
    except jwt.InvalidTokenError:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid token"
                
            )
    
    
    












