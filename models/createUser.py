from models.database_model import Tutor,Topic, Registered_User, Times
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str


class TutorCreate(BaseModel):
    user_email: str
    average_ratings: Optional[float] = 0.0
    classes: str
    price: float
    average_ratings: float
    times: List[str]
    description: str
    main_languages: str
    prefer_in_person: Optional[bool] = False
    cv_link: Optional[str] = None
    other_languages: Optional[str] = None
    profile_picture_link: Optional[str] = None
    video_link: Optional[str] = None
    topics: List[str] = []
    times: List[str] = []


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
    topics = []
    times_available = []
    try:
        for topic in user.topics:
            topics.append(getTopicsByName(topic, db))
        for time in user.times:
            times_available.append(Times(day=time))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    new_tutor = Tutor(user_email = user.user_email, topics=topics, cv_link=user.cv_link, 
                      description=user.description, classes=user.classes, price=user.price, 
                      main_languages=user.main_languages, prefer_in_person=user.prefer_in_person,
                      other_languages=user.other_languages, average_ratings=user.average_ratings, 
                      times=times_available, profile_picture_link=user.profile_picture_link,
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
    try:
        print(f"Getting topic{name}")
        topic = db.query(Topic).filter(Topic.name == name).first()
        print(f"Got topic {topic}")
        # Handle the result or perform further operations
        return topic
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {str(e)}")
