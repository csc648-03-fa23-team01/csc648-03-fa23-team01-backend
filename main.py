
from fastapi import FastAPI, Depends, HTTPException, status
from models.database_model import Base, engine, Tutor, SessionLocal,Topic, tutor_topic_association, Message,Registered_User, Times
from models.sampleInsert import populate_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware
from models.createUser import createUser, createTutorHelper, getUsersByEmail, viewTopics
from models.createUser import UserCreate, TutorCreate
from models.search import searchTutorsTopics, searchTutorsClasses, searchTutorsLanguage, searchTutorsAll, SearchInput, getUserTutors
from typing import Optional  # Import statement added here
from fastapi import HTTPException
from sqlalchemy.orm import Session,contains_eager
from pydantic import BaseModel, Field
from models.database_model import Registered_User
from sqlalchemy.exc import IntegrityError

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
            "times_available": new_tutor.times,
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
            "receiver_profile_pic":message.receiver.tutor.profile_picture_link,
            "sender_first_name":message.sender.first_name,
            "sender_last_name":message.sender.last_name,

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
        user_data = user.to_dict()  # Assuming you have a method to convert the user object to a dictionary
        
        # Check if the user is a tutor and fetch tutor data if they are
        tutor = db.query(Tutor).filter(Tutor.user_email == user.email).first()
        if tutor:
            tutor_data = tutor.to_dict()  # Convert the tutor object to a dictionary
            user_data["tutor"] = tutor_data  # Add tutor data to the user data
        
        # Return the user data, with tutor data if applicable
        return {"user": user_data}
    else:
        # If no user is found, return an appropriate message
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/updateUserStatus")
async def update_user_status(email: str, verified: bool, admin: bool, db: Session = Depends(get_db)):
    try:
        # Fetch the user from the database
        user = db.query(Registered_User).filter(Registered_User.email == email).one()

        # Update the user's status
        user.verified_status = verified
        user.admin_status = admin

        # Commit the changes to the database
        db.commit()

        return {"message": f"User status updated successfully for {email}"}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

class UserUpdateRequest(BaseModel):
    email: Optional[str] = Field(None, example="user@example.com")
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    # Other fields as necessary


@app.patch("/user/{user_id}")
def update_user(user_id: int, update_data: UserUpdateRequest, db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(Registered_User).filter(Registered_User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        # Update fields if they are provided in the request
        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        # Add other fields updates as necessary

        # Commit the changes to the database
        db.commit()  # This will automatically begin a transaction if one hasn't been started
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.refresh(user)

    return user

@app.patch("/tutor/{user_email}", response_model=TutorCreate)
def update_tutor(user_email: str, update_data: TutorCreate, db: Session = Depends(get_db)):
    tutor = db.query(Tutor).filter(Tutor.user_email == user_email).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")

    # Update tutor data
    for var, value in vars(update_data).items():
        if value is not None:
            setattr(tutor, var, value)

    db.commit()
    db.refresh(tutor)
    return tutor
