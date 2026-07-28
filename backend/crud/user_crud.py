from schemas.user_schemas import CreateUser
from models.user_model import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.security import get_password_hashed


#hämtar en user obejct från databasen via unik username
def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def register_user(db: Session, user: CreateUser):
    
    existing_user = get_user_by_username(username = user.username, db = db)
    
    if existing_user:
        return HTTPException(
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
    
    
    
