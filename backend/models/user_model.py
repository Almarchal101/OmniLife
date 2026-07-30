from sqlalchemy import String, Integer, Table, Column, DateTime
from core.database import Base
from core.security import generate_ulid



class BaseModel(Base):
    
    __abstract__ = True
    
    id = Column(String, primary_key = True, default = generate_ulid)
    
    
class User(BaseModel):
    
    __tablename__ = "users"
    
    name = Column(String(50), nullable = False)
    lastname = Column(String(50), nullable = False)
    username = Column(String(100), nullable =False, unique = True)
    age = Column(Integer, nullable = False)
    email = Column(String(140), nullable = False, unique = True)
    gender = Column(String, nullable = True)
    phone_number = Column(String(14), nullable = True, unique = True)
    hashed_password = Column(String, nullable = False)
    
    
class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    jti = Column(String, primary_key=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    
    
    
    
    
