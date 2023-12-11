from models.database_model import Tutor,Topic, Registered_User
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str


class TutorCreate(BaseModel):
    user_email: str
    topics: List[str]
    cv_link: str
    description: str
    classes: str
    price: float
    average_ratings: float
    times_available: str
    main_languages: str
    prefer_in_person: bool
    other_languages: str
    profile_picture_link: str
    video_link: str

def createUser(user: UserCreate, db: Session):
    new_user = Registered_User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        admin_status=False,
        verified_status=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # This is optional

    return new_user

def createTutorHelper(user:TutorCreate, db: Session):
    Topics = []
    for topic in user.topics:
        Topics.append(getTopicsByName(topic, db))
    new_tutor = Tutor(user_email = user.user_email, topics=Topics, cv_link=user.cv_link, 
                      description=user.description, classes=user.classes, price=user.price, 
                      main_languages=user.main_languages, prefer_in_person=user.prefer_in_person,
                      other_languages=user.other_languages, average_ratings=user.average_ratings, 
                      times_available=user.times_available, profile_picture_link=user.profile_picture_link,
                      video_link=user.video_link)
    db.add(new_tutor)
    db.commit()
    db.refresh(new_tutor)
    return new_tutor



def getUsersByEmail(email: str, db: Session):
    print(db.query(Tutor).join(Registered_User).filter(Registered_User.email == email.replace("%40","@")).first())
    return db.query(Tutor).join(Registered_User).filter(Registered_User.email == email.replace("%40","@")).first()

def viewTopics(db: Session):
    return db.query(Topic).all()

def getTopicsByName(name: str, db: Session):
    return db.query(Topic).filter(Topic.name == name).first()
