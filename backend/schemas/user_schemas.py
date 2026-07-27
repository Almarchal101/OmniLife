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
    