
from models.database_model import  Tutor,Topic, tutor_topic_association, Message,Registered_User
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel

class SearchInput(BaseModel):
    text: str

def searchTutorsTopics(text: str, db: Session):
    return db.query(Tutor).join(tutor_topic_association).join(Topic).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times) ).filter(Topic.name.contains(text)).all()

def searchTutorsClasses(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times) ).filter(Tutor.classes.contains(text)).all()

def searchTutorsLanguage(text: str, db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times) ).filter(Tutor.main_languages.contains(text)).all()

def searchTutorsAll(db: Session):
    return db.query(Tutor).options(joinedload(Tutor.user),joinedload(Tutor.topics),joinedload(Tutor.times)).all()

def getUserTutors(user_id: str, db: Session):
    query = db.query(Tutor).join(
        Message, Tutor.user_email == Message.receiver_id
    ).filter(
        Message.sender_id == user_id
    ).distinct()

    return query.all()