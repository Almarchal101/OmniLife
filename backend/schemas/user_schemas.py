from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name : str
    lastname : str
    username : str
    age : int
    email : EmailStr
    gender: str
    phone_number: str 
    password: str
    
class UserOut(BaseModel):
    id: str
    name : str
    lastname : str
    username: str
    
class Authenticate_data(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RefreshToken(BaseModel):
    refresh_token: str