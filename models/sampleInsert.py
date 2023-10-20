from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from models.database_model import Registered_User, Tutor, Topic, TutorTopic, Message
from dotenv import load_dotenv
import os

def populate_db():
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create some sample data
    # Adding Registered Users
    user1 = Registered_User(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        password='password123'
    )
    user2 = Registered_User(
        first_name='Jane',
        last_name='Doe',
        email='jane.doe@example.com',
        password='password123'
    )
    session.add(user1)
    session.add(user2)

    # Adding Tutors
    tutor1 = Tutor(
        user=user1,
        description='Experienced Math Tutor',
        price=30.0
    )
    tutor2 = Tutor(
        user=user2,
        description='Physics Expert',
        price=35.0
    )
    session.add(tutor1)
    session.add(tutor2)

    # Adding Topics
    topic1 = Topic(name='Math')
    topic2 = Topic(name='Physics')
    session.add(topic1)
    session.add(topic2)

    # Adding Tutor-Topic Associations
    tutor_topic1 = TutorTopic(tutor=tutor1, topic=topic1)
    tutor_topic2 = TutorTopic(tutor=tutor2, topic=topic2)
    session.add(tutor_topic1)
    session.add(tutor_topic2)

    # Adding Messages
    message1 = Message(
        who_sent=user1.id,
        message_text='Hello, can we schedule a session for next Monday?',
        sender=user1
    )
    message2 = Message(
        who_sent=user2.id,
        message_text='Sure, see you then!',
        sender=user2
    )
    session.add(message1)
    session.add(message2)

    # Commit and close
    session.commit()
    session.close()

if __name__ == '__main__':
    populate_db()
