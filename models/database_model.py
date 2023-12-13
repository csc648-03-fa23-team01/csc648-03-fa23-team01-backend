from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
import datetime

# Use os.getenv for safer handling of environment variables
database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")  # Add a default URL

engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

tutor_topic_association = Table(
    'tutor_topic',
    Base.metadata,
    Column('tutor_email', String(255) , ForeignKey('Tutors.user_email'), primary_key=True),
    Column('topic_name', String(255) , ForeignKey('Topics.name'), primary_key=True)
)

tutor_time_association = Table(
    'tutor_time',
    Base.metadata,
    Column('tutor_id', String(255), ForeignKey('Tutors.user_email'), primary_key=True),
    Column('time_id', Integer, ForeignKey('Times.id'), primary_key=True)
)

class Registered_User(Base):
    __tablename__ = 'Registered_Users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(255), unique=True)  # Ensure uniqueness
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    admin_status = Column(Boolean, default=False)
    verified_status = Column(Boolean, default=False)
    tutor = relationship("Tutor", uselist=False, back_populates="user")
    messages_sent = relationship("Message", foreign_keys="[Message.sender_id]")
    messages_received = relationship("Message", foreign_keys="[Message.receiver_id]")
    
class Tutor(Base):
    __tablename__ = 'Tutors'

    user_email = Column(String(255), ForeignKey('Registered_Users.email'), primary_key=True)
    average_ratings = Column(Float, default=0.0)
    classes = Column(String(512))
    description = Column(String(512))
    price = Column(Float, default=0.0)
    main_languages = Column(String(255))
    prefer_in_person = Column(Boolean, default=False)
    cv_link = Column(String(512))
    other_languages = Column(String(255))
    profile_picture_link = Column(String(512))
    video_link = Column(String(512))
    
    user = relationship("Registered_User", back_populates="tutor")
    topics = relationship('Topic', secondary=tutor_topic_association, back_populates='tutors')
    times = relationship('Times', secondary=tutor_time_association, back_populates='tutors')


class Topic(Base):
    __tablename__ = 'Topics'
    name = Column(String(255), nullable=False, primary_key=True)
    
    # Relationship to the TutorTopic association model
    tutors = relationship('Tutor', secondary=tutor_topic_association, back_populates='topics')

class Times(Base):
    __tablename__ = 'Times'

    id = Column(Integer, primary_key=True)
    day = Column(String(255), nullable=False)
    tutors = relationship('Tutor', secondary=tutor_time_association, back_populates='times')


class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('Registered_Users.id'))
    receiver_id = Column(Integer, ForeignKey('Registered_Users.id'))
    message_text = Column(Text, nullable=False)
    when_sent = Column(DateTime, default=datetime.datetime.utcnow)  # Changed to datetime.now for timezone awareness

    sender = relationship("Registered_User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("Registered_User", foreign_keys=[receiver_id], back_populates="messages_received")

