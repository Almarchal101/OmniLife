from fastapi import APIRouter, Depends
from schemas.user_schemas import UserOut, CreateUser
from sqlalchemy.orm import session
from core.database import get_db
from crud.user_crud import register_user

user_api_router = APIRouter(prefix = "/user")


@user_api_router.post("/create", response_model = UserOut)
def create_user(user: CreateUser, db: session = Depends(get_db)):
    return register_user(db, user)