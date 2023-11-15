
from fastapi import FastAPI, Depends, HTTPException
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association, Message,Registered_User
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from models.createUser import createUser, createTutorHelper, getUsersByEmail, viewTopics
from models.createUser import UserCreate, TutorCreate
from models.search import searchTutorsTopics, searchTutorsClasses, searchTutorsLanguage, searchTutorsAll, SearchInput, getUserTutors

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def gen():
    Base.metadata.create_all(engine)

@app.get("/populate")
async def populate():
    populate_response = populate_db()
    if populate_response == 'Database populated successfully':
        return {"message": "Database populated successfully"}
    else:
        raise HTTPException(status_code=500, detail=populate_response)
    

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

@app.get("/userTutors")
async def getUserTutors(user_id: str, db: Session = Depends(get_db)):
    tutors = getUserTutors(user_id, db)
    return tutors

# create a new user
@app.post("/createUsers", response_model=UserCreate)
async def createUsers(user:UserCreate, db: Session = Depends(get_db))-> Registered_User:
    registered_userEmail = getUsersByEmail(user.email, db)
    if  registered_userEmail:
            raise HTTPException(status_code=400, detail="User already registered")
    new_user = createUser(user, db)

    return new_user

@app.get("/tutor")
async def fetchTutors(id:int, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).join(Registered_User, Tutor.user_email == Registered_User.email) \
    .options(joinedload(Tutor.user), joinedload(Tutor.topics), joinedload(Tutor.times)) \
    .filter(Registered_User.id == id) \
    .first()
    if tutor:
        return tutor
    else:
        print("No tutor found with that ID.")
        return None
  
# create a new tutor
@app.post("/createTutor", response_model=None)
async def createTutor(user:TutorCreate, db: Session = Depends(get_db))-> Tutor:
    new_tutor = createTutorHelper(user, db)
    topics = [topic.name for topic in new_tutor.topics]
    return {
        "email": new_tutor.user_email,
        "topics": topics,
        "cv_link": new_tutor.cv_link,
        "description": new_tutor.description,
        "classes": new_tutor.classes,
        "price": new_tutor.price,
        "average_ratings": new_tutor.average_ratings,
        "times_available": new_tutor.times_available,
        "main_languages": new_tutor.main_languages,
        "prefer_in_person": new_tutor.prefer_in_person,
        "other_languages": new_tutor.other_languages,
        "profile_picture_link": new_tutor.profile_picture_link,
        "video_link": new_tutor.video_link
    }
    


#get user's information
@app.post("/user/{user_email}")
def get_user_with_messages(user_email: str, db: Session = Depends(get_db)):
    
    user = getUsersByEmail(user_email, db)
    messages = [message.message_text for message in user.messages]
    
    return {
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "adminStatus": user.admin_status,
        "verifiedStatus": user.verified_status,
        "messages": messages
    }

# get all topics
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
