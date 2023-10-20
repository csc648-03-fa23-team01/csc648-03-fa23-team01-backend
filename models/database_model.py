from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import os
from alchemical import Alchemical

import datetime

engine = create_engine(os.environ["DATABASE_URL"], echo=True)
Base = declarative_base()

class Registered_User(Base):
    __tablename__ = 'Registered_Users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    admin_status = Column(Boolean, default=False)
    profile_picture_link = Column(String(512))
    verified_status = Column(Boolean, default=False)

    tutor = relationship("Tutor", uselist=False, back_populates="user")
    messages = relationship("Message", back_populates="sender")

class Tutor(Base):
    __tablename__ = 'Tutors'

    user_id = Column(Integer, ForeignKey('Registered_Users.id'), primary_key=True)
    average_ratings = Column(Float, default=0.0)
    classes = Column(String(512))
    description = Column(String(512))
    price = Column(Float, default=0.0)
    times_available = Column(String(512))
    main_languages = Column(String(255))
    prefer_in_person = Column(Boolean, default=False)
    cv_link = Column(String(512))
    other_languages = Column(String(255))

    user = relationship("Registered_User", back_populates="tutor")
    topics = relationship('TutorTopic', back_populates='tutor')

class Topic(Base):
    __tablename__ = 'Topics'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    # Relationship to the TutorTopic association model
    tutors = relationship('TutorTopic', back_populates='topic')

class TutorTopic(Base):
    __tablename__ = 'tutor_topic_association'

    tutor_id = Column(Integer, ForeignKey('Tutors.user_id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('Topics.id'), primary_key=True)

    tutor = relationship('Tutor', back_populates='topics')
    topic = relationship('Topic', back_populates='tutors')


class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True)
    receiver = Column(Integer, ForeignKey('Registered_Users.id'))
    message_text = Column(Text, nullable=False)
    when_sent = Column(DateTime, default=datetime.datetime.utcnow)
    message_id = Column(Integer, unique=True)
    sender = relationship("Registered_User", back_populates="messages")

