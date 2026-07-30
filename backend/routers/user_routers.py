from fastapi import APIRouter, Depends
from schemas.user_schemas import UserOut, CreateUser, Token, Authenticate_data, RefreshToken
from sqlalchemy.orm import session
from core.database import get_db
from crud.user_crud import *



user_api_router = APIRouter(prefix = "/user")


@user_api_router.post("/create", response_model = UserOut)
def create_user(user: CreateUser, db: session = Depends(get_db)):
    return register_user(db, user)


@user_api_router.post("/login", response_model = Token)
def login_user(user: Authenticate_data, db: session = Depends(get_db)):
    return authenticate_user(user, db)


@user_api_router.delete("/delete")
def remove_my_account(username: str, current_user: User = Depends(get_current_user), db: session = Depends(get_db)):
    
    if current_user.username != username:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "you can not remove this account"
        ) 
        
    return delete_my_account(username = username, db = db)

@user_api_router.post("/logout")
def logout_user(token: str = Depends(settings.oauth2_scheme),db: session = Depends(get_db)):
    return logout(token = token, db = db)


@user_api_router.post("/refresh", response_model = Token)
def refresh_user_access_token(data: RefreshToken, db: session = Depends(get_db)):
    return refresh_access_token(data = data, db = db)
