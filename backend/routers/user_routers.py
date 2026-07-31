from fastapi import APIRouter, Depends, Request
from schemas.user_schemas import UserOut, CreateUser, Token, Authenticate_data, RefreshToken
from sqlalchemy.orm import session
from core.database import get_db
from crud.user_crud import *
from core.api_limiter import limiter



user_api_router = APIRouter(prefix = "/user")


@user_api_router.post("/create", response_model = UserOut)
@limiter.limit("5/minute")
def create_user(request: Request  ,user: CreateUser, db: session = Depends(get_db)):
    return register_user(db, user)


@user_api_router.post("/login", response_model = Token)
@limiter.limit("5/minute")
def login_user(request: Request, user: Authenticate_data, db: session = Depends(get_db)):
    return authenticate_user(user, db)


@user_api_router.delete("/delete")
@limiter.limit("5/minute")
def remove_my_account(request: Request, username: str, current_user: User = Depends(get_current_user), db: session = Depends(get_db)):
    
    if current_user.username != username:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "you can not remove this account"
        ) 
        
    return delete_my_account(username = username, db = db)

@user_api_router.post("/logout")
@limiter.limit("5/minute")
def logout_user(request: Request, token: str = Depends(settings.oauth2_scheme),db: session = Depends(get_db)):
    return logout(token = token, db = db)


@user_api_router.post("/refresh", response_model = Token)
@limiter.limit("5/minute")
def refresh_user_access_token(request: Request, data: RefreshToken, db: session = Depends(get_db)):
    return refresh_access_token(data = data, db = db)
