
from fastapi import FastAPI, Depends, HTTPException
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association, Message,Registered_User
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload, contains_eager
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
    try:
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
    except IntegrityError as e:
        if e and 'Duplicate entry' in str(e):
            raise HTTPException(status_code=400, detail="User already exist in Database")
        else:
            raise HTTPException(status_code=400, detail=f'Error: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error: {e}')


#get user's information
@app.post("/user/{user_email}")
def get_user_with_messages(user_email: str, db: Session = Depends(get_db)):
    
    user = db.query(Tutor)\
        .join(Registered_User)\
        .filter(Registered_User.email == user_email.replace("%40","@"))\
        .first()
    print("\n\n",user)
    if(user):
        return {
            "email": user.email,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "adminStatus": user.admin_status,
            "verifiedStatus": user.verified_status,
            "user_id":user.id,
            "data":user
        }
    else:
        return None

# get all topics
@app.get("/getTopics")
async def getTopics(db: Session = Depends(get_db)):
    return viewTopics(db)



@app.post("/message")
async def postMessage(sender_id: str, receiver_id: str, text: str, db: Session = Depends(get_db)):
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

@app.get("/messages/sent/{user_id}")
async def get_sent_messages(user_id: str, db: Session = Depends(get_db)):
    # Query the database for messages where the sender_id matches the given user ID
    messages = db.query(Message).filter(Message.sender_id == user_id).all()

    # Check if any messages were found
    if messages:
        # Convert messages to a suitable format for JSON response (if necessary)
        response = [{
            "id": message.id,
            "receiver_id": message.receiver_id,
            "message_text": message.message_text,
            "when_sent": message.when_sent.isoformat()  # format datetime for JSON
        } for message in messages]
        return response
    else:
        raise HTTPException(status_code=404, detail="No messages sent by this user")


@app.get("/messages/sent/byemail/{user_email}")
async def get_sent_messages_by_email(user_email: str, db: Session = Depends(get_db)):
    
    user = db.query(Registered_User).filter(Registered_User.email == user_email).first()

    if user:
        messages = db.query(Message)\
            .join(Registered_User, Message.sender_id == Registered_User.id)\
            .outerjoin(Tutor, Registered_User.email == Tutor.user_email)\
            .options(contains_eager(Message.sender))\
            .filter(Message.sender_id == user.id)\
            .all()
        # Process the messages to include tutor information
        messages_with_tutor_info = []
        for message in messages:
            message_data = {
                'content': message.message_text,
                'sender_email': message.sender.email,
                'sender_name': f"{message.sender.first_name} {message.sender.last_name}",
                # Add additional message fields as needed
            }

            # Check if the sender is a tutor and add tutor info
            if message.receiver.tutor:
                message_data['tutor_info'] = {
                    'average_ratings': message.receiver.tutor.average_ratings,
                    'main_languages': message.receiver.tutor.main_languages,
                    # Add additional tutor fields as needed
                }
    else:
        messages_with_tutor_info = []
    if messages:
        print(messages)
        response = [{
            "id": message.id,
            "receiver_id": message.receiver_id,
            "message_text": message.message_text,
            "when_sent": message.when_sent.isoformat(),
            "receiver_first_name":message.receiver.first_name,
            "receiver_last_name":message.receiver.last_name,
            "receiver_profile_pic":message.receiver.tutor.profile_picture_link
        } for message in messages]
        return response
    else:
        return {"message": "No messages sent by this user"}
    
@app.get("/getUserByEmail")
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    # Query the database for the user based on the email
    user = db.query(Registered_User).filter(Registered_User.email == email.replace("%40","@")).first()

    # Check if the user exists
    if user:
        # Return the user ID
        return {"user": user}
    else:
        # If no user is found, return an appropriate message
        raise HTTPException(status_code=404, detail="User not found")
