from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Registered_User(Base):
    __tablename__ = 'Registered_Users'

    id = Column('ID', Integer, primary_key=True)
    first_name = Column('First_Name', String(255), nullable=False)
    last_name = Column('Last_Name', String(255), nullable=False)
    email = Column('Email', String(255), nullable=False, unique=True)
    password = Column('Password', String(255), nullable=False)
    admin_status = Column('Admin_Status', Boolean, default=False)
    profile_picture_link = Column('Profile_Picture_Link', String(512))
    verified_status = Column('Verified_Status', Boolean, default=False)

    tutor = relationship("Tutor", uselist=False, back_populates="user")
    messages = relationship("Message", back_populates="sender")

class Tutor(Base):
    __tablename__ = 'Tutors'

    user_id = Column('User_ID', Integer, ForeignKey('Registered_Users.ID'), primary_key=True)
    average_ratings = Column('Average_Ratings', Float, default=0.0)
    classes = Column('Classes', String(512))
    description = Column('Description', String(512))
    price = Column('Price', Float, default=0.0)
    times_available = Column('Times_Available', String(512))
    main_languages = Column('Main_Languages', String(255))
    prefer_in_person = Column('Prefer_in_person', Boolean, default=False)
    cv_link = Column('CV_Link', String(512))
    other_languages = Column('Other_Languages', String(255))

    user = relationship("Registered_User", back_populates="tutor")

class Message(Base):
    __tablename__ = 'Messages'

    id = Column('ID', Integer, primary_key=True)
    who_sent = Column('Who_Sent', Integer, ForeignKey('Registered_Users.ID'))
    message_text = Column('Message_Text', Text, nullable=False)
    when_sent = Column('When_Sent', DateTime, default=datetime.datetime.utcnow)
    message_id = Column('Message_ID', Integer, unique=True)

    sender = relationship("v", back_populates="messages")


# Create the tables
if __name__ == '__main__':
    DATABASE_URI = 'mysql+mysqldb://root:password@localhost:3306/test?charset=utf8'
    engine = create_engine(DATABASE_URI, echo=True)  # echo=True will show generated SQL statements
    Base.metadata.create_all(engine)
