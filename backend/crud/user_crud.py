from schemas.user_schemas import Authenticate_data, CreateUser, Token
from models.user_model import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.security import get_password_hashed, create_access_token, create_refresh_token, verify_password
from pydantic import EmailStr



#hämtar en user obejct från databasen via unik username
def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(email: EmailStr , db: Session):
    return db.query(User).filter(User.email == email).first()

def register_user(db: Session, user: CreateUser):
    
    existing_user = get_user_by_username(username = user.username, db = db)
    
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"The user with id: {user.id} already exists",
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
    

    
    
        


    
    
