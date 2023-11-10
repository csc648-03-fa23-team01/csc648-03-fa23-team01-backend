from fastapi import FastAPI, Depends, HTTPException
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association, Registered_User
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from models.createUser import createUser, createTutorHelper, getUsersByEmail, viewTopics
from models.createUser import UserCreate, TutorCreate
from models.search import searchTutorsTopics, searchTutorsClasses, searchTutorsLanguage, searchTutorsAll, SearchInput

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
    populate_db()
    return {"message": "Database populated"}

# search tutors by topic, classes, language, or all
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

# create a new user
@app.post("/createUsers", response_model=UserCreate)
async def createUsers(user:UserCreate, db: Session = Depends(get_db))-> Registered_User:
    registered_userEmail = getUsersByEmail(user.email, db)
    if  registered_userEmail:
            raise HTTPException(status_code=400, detail="User already registered")
    new_user = createUser(user, db)

    return new_user

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
        "other_languages": new_tutor.other_languages
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
        "profilePictureLink": user.profile_picture_link,
        "adminStatus": user.admin_status,
        "verifiedStatus": user.verified_status,
        "messages": messages
    }

# get all topics
@app.get("/getTopics")
async def getTopics(db: Session = Depends(get_db)):
    return viewTopics(db)