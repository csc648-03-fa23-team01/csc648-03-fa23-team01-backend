from fastapi import FastAPI, Depends
from models.database_model import Base, engine, Tutor, SessionLocal
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
   "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def gen():
    Base.metadata.create_all(engine)

@app.get("/populate")
async def populate():
    populate_db()
    return {"message": "Database populated"}

@app.post("/search")
async def searchTutors(input: SearchInput, db: Session = Depends(get_db)):
    tutors = searchTutorsTopics(input.text, db)
    return tutors
