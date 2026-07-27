from fastapi import FastAPI
from core.database import Base, engine 
from core.security import generate_ulid

Base.metadata.create_all(bind = engine) #createing all tables 

app = FastAPI()

@app.get('/')
def home():
    return {'hej': 'welcome'}