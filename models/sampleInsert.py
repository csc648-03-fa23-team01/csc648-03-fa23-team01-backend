from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from models.database_model import Registered_User, Tutor, Message
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

#use to populate local tables
Base = declarative_base()

if __name__ == '__main__':
    DATABASE_URI = 'mysql+mysqldb://root:password@localhost:3306/DB_NAME'
    engine = create_engine(DATABASE_URI, echo=True)  # echo=True will show generated SQL statements
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    john = Registered_User(first_name='John', last_name='Doe', email='john.doe@example.com', password='hashed_password_1', admin_status=False, profile_picture_link='http://example.com/profile1.jpg', verified_status=True)
    jane = Registered_User(first_name='Jane', last_name='Smith', email='jane.smith@example.com', password='hashed_password_2', admin_status=True)
    alice = Registered_User(first_name='Alice', last_name='Johnson', email='alice.johnson@example.com', password='hashed_password_3', admin_status=False, profile_picture_link='http://example.com/profile3.jpg', verified_status=True)

    session.add_all([john, jane, alice])
    session.commit()

    # Inserting data into Tutors
    john_tutor = Tutor(user_id=john.id, average_ratings=4.5, classes='Math, Physics', description='Experienced tutor with 5 years of teaching.', price=30.00, times_available='Weekdays 4pm-6pm', main_languages='English', prefer_in_person=True, cv_link='http://example.com/cv1.pdf', other_languages='French, Spanish')
    alice_tutor = Tutor(user_id=alice.id, average_ratings=4.0, classes='English, Literature', description='Passionate about languages and literature.', price=25.00, times_available='Weekends 10am-1pm', main_languages='English', other_languages='German')

    session.add_all([john_tutor, alice_tutor])
    session.commit()

    # Inserting data into Messages
    message_1 = Message(who_sent=john.id, message_text='Hello, I would like to book a session.', when_sent=datetime.datetime.now(), message_id=1001)
    message_2 = Message(who_sent=alice.id, message_text='Sure, let\'s schedule a time.', when_sent=datetime.datetime.now(), message_id=1002)

    session.add_all([message_1, message_2])
    session.commit()
    session.close()


# Closing the session
