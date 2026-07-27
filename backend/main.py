from fastapi import FastAPI
from core.database import Base, engine 
from routers.user_routers import user_api_router


Base.metadata.create_all(bind = engine) #createing all tables 

app = FastAPI()
app.include_router(user_api_router)
@app.get('/')
def home():
    return {'hej': 'welcome'}