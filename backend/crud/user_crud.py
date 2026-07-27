from schemas.user_schemas import CreateUser
from models.user_model import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def register_user(db: Session, user: CreateUser):
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    if existing_user:
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail=f"The user with id: {user.id} already exists",
        )
    
    new_user = User( 
                    name = user.name,
                    lastname = user.lastname,
                    username = user.username,
                    age = user.age, 
                    email = user.email,
                    gender = user.gender,
                    phone_number = user.phone_number,
                    hased_password = user.password)
    
    db.add(new_user)
    db.commit()
    
    return new_user
    
    
    
