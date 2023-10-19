from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from alchemical import Alchemical

import datetime
db = Alchemical('mysql+mysqlconnector://root:Isagi11*@localhost:3306/sqlalchemy')


class Registered_User(db.Model):
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

class Tutor(db.Model):
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

class Message(db.Model):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True)
    who_sent = Column(Integer, ForeignKey('Registered_Users.id'))
    message_text = Column(Text, nullable=False)
    when_sent = Column(DateTime, default=datetime.datetime.utcnow)
    message_id = Column(Integer, unique=True)
    sender = relationship("Registered_User", back_populates="messages")


#Uncomment to create local tables
# if __name__ == '__main__':
#     DATABASE_URI = 'mysql+mysqldb://root:password@localhost:3306/tablename'
#     engine = create_engine(DATABASE_URI, echo=True)  # echo=True will show generated SQL statements
#     Base.metadata.create_all(engine)
    
    