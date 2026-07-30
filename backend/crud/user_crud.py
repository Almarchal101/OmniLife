from schemas.user_schemas import Authenticate_data, CreateUser, Token, RefreshToken
from models.user_model import *
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from core.security import *
from pydantic import EmailStr





#hämtar en user obejct från databasen via unik username
def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(email: EmailStr , db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_phone_number(phone_number: str , db: Session):
    return db.query(User).filter(User.phone_number == phone_number).first()

def get_user_by_id(id: str , db: Session):
    return db.query(User).filter(User.id == id).first()




def register_user(db: Session, user: CreateUser):
    
    if get_user_by_username(username=user.username, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The username '{user.username}' is already taken",
        )
        

    if get_user_by_email(email=user.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The email '{user.email}' is already registered",
        )
        

    if get_user_by_phone_number(phone_number=user.phone_number, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The phone number '{user.phone_number}' is already registered",
        )
    
    hashed_password = get_password_hashed(user.password)
    
    new_user = User( 
                    name = user.name,
                    lastname = user.lastname,
                    username = user.username,
                    age = user.age, 
                    email = user.email,
                    gender = user.gender,
                    phone_number = user.phone_number,
                    hashed_password = hashed_password)
    
    db.add(new_user)
    db.commit()
    
    return new_user


def authenticate_user(data: Authenticate_data, db: Session) -> Token:
    
    existing_user = get_user_by_email(email = data.email, db = db)
    
    
    if not existing_user:
        raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED,
              detail=f" Wrong email or password",
          )
        
    if not verify_password(data.password, existing_user.hashed_password):
         raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail=f" Wrong email or password",
        )
         
    access_token = create_access_token(existing_user.id)
    refresh_token = create_refresh_token(existing_user.id)
    
    
    return Token(
        access_token = access_token,
        refresh_token = refresh_token,
    )
    
    
def delete_my_account(username: str, db: Session):
    
    existing_user = get_user_by_username(username = username, db = db)
    
    if not existing_user:
        raise HTTPException(
              status_code = status.HTTP_401_UNAUTHORIZED,
              detail=f" The user with username: {username} not found",
          )
        
        
    db.delete(existing_user)
    db.commit()
    
    return {"success": f"your account has been removed"}


def get_current_user(
    token: str = Depends(settings.oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token, expected_type = "access_token")


    jti = payload["jti"]
    if db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token har blivit återkallad")


    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Användaren finns inte längre")

    return user


def logout(token: str, db: Session):
    
    payload = decode_token(token)
    jti = payload['jti']
    expires_at = datetime.fromtimestamp(payload["exp"], tz = timezone.utc)
    
    revoked_token = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
    
    if revoked_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has already been revoked"
        )
        
        
    db.add(RevokedToken(jti=jti, expires_at=expires_at))
    db.commit()
    
    
    return {"success": "you have successfully logged out"}
    

def refresh_access_token(data: RefreshToken, db: Session ):
    
    payload = decode_token(data.refresh_token, expected_type = "refresh_token")
    
    jti = payload['jti']
    
    if db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-token har blivit återkallad"
        )
    
    user_id = payload['sub']
    user = get_user_by_id(user_id, db)
    
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Användaren finns inte längre"
        )
        
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    db.add(RevokedToken(jti=jti, expires_at=expires_at))
    db.commit()

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


    
    
