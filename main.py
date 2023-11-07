from fastapi import FastAPI, Depends
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
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
    return db.query(Tutor).join(tutor_topic_association).join(Topic).options(joinedload(Tutor.user),joinedload(Tutor.topics) ).filter(Topic.name.contains(text)).all()

def searchTutorsClasses(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics) ).filter(Tutor.classes.contains(text)).all()

def searchTutorsLanguage(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics) ).filter(Tutor.main_languages.contains(text)).all()

def searchTutorsAll(db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics)).all()

def fetchTutor(id:int ,db: Session):
    tutor = db.query(Tutor).filter(Tutor.user_id == id).first()
    if tutor:
        print(f"Tutor Found: {tutor.user_id}, {tutor.description}")
        return tutor
    else:
        print("No tutor found with that ID.")
        return None

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

@app.get("/tutors")
async def fetchTutors(id:int, db: Session = Depends(get_db)):
    return fetchTutor(id,db)
    

@app.post("/search")
async def searchTutors(type: str, input: SearchInput, db: Session = Depends(get_db)):
    print(type)
    if(type == "Subject"):
        tutors = searchTutorsTopics(input.text, db)
    elif (type == "Classes"):
        tutors = searchTutorsClasses(input.text, db)
    elif (type == "Language"):
        tutors = searchTutorsLanguage(input.text, db)
    else:
        tutors = searchTutorsAll(db)
    return tutors
