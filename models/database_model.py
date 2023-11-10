from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from alchemical import Alchemical
from sqlalchemy import UniqueConstraint

import datetime

db = Alchemical(os.environ["DATABASE_URL"])
engine = create_engine(os.environ["DATABASE_URL"], echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

tutor_topic_association = Table(
    'tutor_topic',
    Base.metadata,
    Column('tutor_email', String(255) , ForeignKey('Tutors.user_email'), primary_key=True),
    Column('topic_name', String(255) , ForeignKey('Topics.name'), primary_key=True)
)

class Registered_User(Base):
    __tablename__ = 'Registered_Users'

    email = Column(String(255), primary_key= True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    admin_status = Column(Boolean, default=False)
    profile_picture_link = Column(String(512))
    verified_status = Column(Boolean, default=False)

    tutor = relationship("Tutor", uselist=False, back_populates="user")
    messages = relationship("Message", back_populates="sender")

class Tutor(Base):
    __tablename__ = 'Tutors'

    user_email = Column(String(255), ForeignKey('Registered_Users.email'), primary_key=True)
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
    topics = relationship('Topic', secondary=tutor_topic_association, back_populates='tutors')


class Topic(Base):
    __tablename__ = 'Topics'
    name = Column(String(255), nullable=False, primary_key=True)
    
    # Relationship to the TutorTopic association model
    tutors = relationship('Tutor', secondary=tutor_topic_association, back_populates='topics')


class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True)
    receiver = Column(String(255), ForeignKey('Registered_Users.email'))
    message_text = Column(Text, nullable=False)
    when_sent = Column(DateTime, default=datetime.datetime.utcnow)
    message_id = Column(Integer, unique=True)
    sender = relationship("Registered_User", back_populates="messages")

