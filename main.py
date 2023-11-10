
from fastapi import FastAPI, Depends
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association, Message,Registered_User
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from models.createUser import createUser, createTutorHelper, getUsersByID, getUsersByEmail, viewTopics
from models.createUser import UserCreate, TutorCreate


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
    return db.query(Tutor).join(tutor_topic_association).join(Topic).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times)).filter(Topic.name.contains(text)).all()

def searchTutorsClasses(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times) ).filter(Tutor.classes.contains(text)).all()

def searchTutorsLanguage(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times)).filter(Tutor.main_languages.contains(text)).all()

def searchTutorsAll(db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times)).all()

def fetchTutor(id:int ,db: Session):
    tutor = db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics)).filter(Tutor.user_id == id).first()
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

@app.get("/tutor")
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


@app.post("/createUsers", response_model=UserCreate)
async def createUsers(user:UserCreate, db: Session = Depends(get_db))-> Registered_User:
    registered_userID = getUsersByID(user.id, db)
    registered_userEmail = getUsersByEmail(user.email, db)
    if registered_userID or registered_userEmail:
            raise HTTPException(status_code=400, detail="User already registered")
    new_user = createUser(user, db)

    return new_user


@app.post("/createTutor", response_model=None)
async def createTutor(user:TutorCreate, db: Session = Depends(get_db))-> Tutor:
    new_tutor = createTutorHelper(user, db)
    return new_tutor



@app.post("/user/{user_id}")
def get_user_with_messages(user_id: str, db: Session = Depends(get_db)):
    
    user = getUsersByID(user_id, db)
    messages = [message.message_text for message in user.messages]
    
    return {
        "id": user.id,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "password": user.password,
        "profilePictureLink": user.profile_picture_link,
        "adminStatus": user.admin_status,
        "verifiedStatus": user.verified_status,
        "messages": messages
    }

@app.get("/getTopics")
async def getTopics(db: Session = Depends(get_db)):
    return viewTopics(db)
@app.post("/message")
async def postMessage(sender_id: int, receiver_id: int, text: str, db: Session = Depends(get_db)):
    # Check if sender and receiver exist
    sender = db.query(Registered_User).filter(Registered_User.id == sender_id).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    receiver = db.query(Registered_User).filter(Registered_User.id == receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Create a new message instance
    new_message = Message(
        receiver_id=receiver_id,
        message_text=text,
        sender_id=sender_id
    )

    # Add the new message to the database session and commit
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message
