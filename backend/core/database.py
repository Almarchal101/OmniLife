from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./test.db" # var databasen ska finnas 
engine = create_engine(DATABASE_URL) #kopplinen mellann koden och data basen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #för att kunna göra databas anrop skapade radera osv
Base = declarative_base() #så arr sqlalchey vet vilka tabllers som ska skapas 




# Dependeci för att öpnna och stänga databasen connection 
def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
        
