from fastapi import FastAPI, Depends
from alchemical import Alchemical
from models.database_model import Registered_User, Tutor, Message, SessionLocal
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy import select
from pydantic import BaseModel
app = FastAPI()
db = Alchemical('mysql+mysqldb://root:1234@localhost:3306/tutorial_db?charset=utf8')

print("hello world")
class SearchInput(BaseModel):
    text: str
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def searchTutorsTopics(text: str, db: Session):
    return db.query(Tutor).filter(Tutor.classes.contains(text)).all()


@app.post("/search")
async def searchTutors(input: SearchInput, db: Session = Depends(get_db)):
    tutors = searchTutorsTopics(input.text, db)
    return tutors