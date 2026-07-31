from fastapi import FastAPI
from core.database import Base, engine 
from core.api_limiter import limiter
from routers.user_routers import user_api_router
from slowapi import  _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


Base.metadata.create_all(bind = engine) #createing all tables 

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(user_api_router)
@app.get('/')
def home():
    return {'hej': 'welcome'}