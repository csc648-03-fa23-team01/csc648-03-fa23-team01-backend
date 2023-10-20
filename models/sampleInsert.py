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
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/jake.jpg'
    )
    user2 = Registered_User(
        first_name='Jane',
        last_name='Doe',
        email='jane.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/jessica.jpg'

    )
    user3 = Registered_User(
        first_name='joe',
        last_name='jo',
        email='joe.jo@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg'

    )
    user4 = Registered_User(
        first_name='bill',
        last_name='Doe',
        email='billy.doe@example.com',
        password='password123'
    )
    user5 = Registered_User(
        first_name='nasd',
        last_name='Doe',
        email='asd.doe@example.com',
        password='password123'
    )
    user6 = Registered_User(
        first_name='John',
        last_name='asd',
        email='johfsdfdsn.doe@example.com',
        password='password123'
    )
    user7 = Registered_User(
        first_name='asff',
        last_name='Doe',
        email='sdgg.doe@example.com',
        password='password123'
    )
    user8 = Registered_User(
        first_name='jhjk',
        last_name='Doe',
        email='jhjk.doe@example.com',
        password='password123'
    )
    user9 = Registered_User(
        first_name='asdasdfsd',
        last_name='Doe',
        email='asdasdfsd.doe@example.com',
        password='password123'
    )
    user10 = Registered_User(
        first_name='jkhygui',
        last_name='Doe',
        email='jkhygui.doe@example.com',
        password='password123'
    )
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.add(user5)
    session.add(user6)
    session.add(user7)
    session.add(user8)
    session.add(user9)
    session.add(user10)
    # Adding Tutors
    tutor1 = Tutor(
        user=user1,
        description='Experienced Math Tutor',
        price=30.0,
        average_ratings=4.5,
        classes='Algebra, Geometry, Calculus',
        times_available='Mon-Fri: 9am-5pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor1.pdf',
        other_languages='Spanish, French'
    )

    tutor2 = Tutor(
        user=user2,
        description='Physics Expert',
        price=35.0,
        average_ratings=4.7,
        classes='Physics I, Physics II',
        times_available='Mon-Wed, Fri: 10am-4pm',
        main_languages='English',
        prefer_in_person=False,
        cv_link='https://example.com/cv/tutor2.pdf',
        other_languages='German'
    )
    tutor3 = Tutor(
        user=user3,
        description='Chemistry Guru',
        price=40.0,
        average_ratings=4.8,
        classes='Organic Chemistry, Inorganic Chemistry',
        times_available='Tue-Thu: 10am-6pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor3.pdf',
        other_languages='Italian, Spanish'
    )
    
    tutor4 = Tutor(
        user=user4,
        description='Biology Expert',
        price=28.0,
        average_ratings=4.6,
        classes='Cell Biology, Genetics',
        times_available='Mon, Wed, Fri: 8am-12pm',
        main_languages='English',
        prefer_in_person=False,
        cv_link='https://example.com/cv/tutor4.pdf',
        other_languages='French'
    )
    tutor5 = Tutor(
        user=user5,
        description='Statistics Whiz',
        price=32.0,
        average_ratings=4.7,
        classes='Intro to Statistics, Advanced Statistics',
        times_available='Mon-Fri: 1pm-4pm',
        main_languages='English',
        prefer_in_person=False,
        cv_link='https://example.com/cv/tutor5.pdf',
        other_languages='Spanish, German'
    )
    tutor6 = Tutor(
        user=user6,
        description='English Literature Enthusiast',
        price=25.0,
        average_ratings=4.3,
        classes='British Literature, American Literature',
        times_available='Tue, Thu: 10am-3pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor6.pdf',
        other_languages='French, Spanish'
    )
    tutor7 = Tutor(
        user=user7,
        description='Experienced Math Tutor',
        price=30.0
    )
    tutor8 = Tutor(
        user=user8,
        description='Physics Expert',
        price=35.0
    )
    tutor9 = Tutor(
        user=user9,
        description='Experienced Math Tutor',
        price=30.0
    )
    tutor10 = Tutor(
        user=user10,
        description='Physics Expert',
        price=35.0
    )
    session.add(tutor1)
    session.add(tutor2)
    session.add(tutor3)
    session.add(tutor4)
    session.add(tutor5)
    session.add(tutor6)
    session.add(tutor7)
    session.add(tutor8)
    session.add(tutor9)
    session.add(tutor10)


    # Adding Topics
    topic1 = Topic(name='Math')
    topic2 = Topic(name='Physics')
    topic3 = Topic(name='Science')
    topic4 = Topic(name='Reading')
    topic5 = Topic(name='English')
    topic6 = Topic(name='Spanish')
    topic7 = Topic(name='umm')
    topic8 = Topic(name='yes')

    session.add(topic1)
    session.add(topic2)
    session.add(topic3)
    session.add(topic4)
    session.add(topic5)
    session.add(topic6)
    session.add(topic7)
    session.add(topic8)

    # Adding Tutor-Topic Associations
    tutor_topic1 = TutorTopic(tutor=tutor1, topic=topic1)
    tutor_topic2 = TutorTopic(tutor=tutor2, topic=topic2)
    tutor_topic3 = TutorTopic(tutor=tutor3, topic=topic3)
    tutor_topic4 = TutorTopic(tutor=tutor4, topic=topic4)
    tutor_topic5 = TutorTopic(tutor=tutor5, topic=topic5)
    tutor_topic6 = TutorTopic(tutor=tutor6, topic=topic6)
    tutor_topic7 = TutorTopic(tutor=tutor7, topic=topic7)
    tutor_topic8 = TutorTopic(tutor=tutor8, topic=topic8)
    session.add(tutor_topic1)
    session.add(tutor_topic2)
    session.add(tutor_topic3)
    session.add(tutor_topic4)
    session.add(tutor_topic5)
    session.add(tutor_topic6)
    session.add(tutor_topic7)
    session.add(tutor_topic8)



    # Adding Messages
    message1 = Message(
        receiver=user1.id,
        message_text='Hello, can we schedule a session for next Monday?',
        sender=user1
    )
    message2 = Message(
        receiver=user2.id,
        message_text='Sure, see you then!',
        sender=user2
    )
    message3 = Message(
        receiver=user1.id,
        message_text='Heasdasd session for next Monday?',
        sender=user1
    )
    message4 = Message(
        receiver=user3.id,
        message_text='Sure, umm!',
        sender=user2
    )
    message5 = Message(
        receiver=user4.id,
        message_text='Hello, bruh?',
        sender=user1
    )
    message6 = Message(
        receiver=user5.id,
        message_text='stop!',
        sender=user2
    )
    message7 = Message(
        receiver=user6.id,
        message_text='nooooo?',
        sender=user2
    )
    message8 = Message(
        receiver=user7.id,
        message_text='asdasdasdasd!',
        sender=user2
    )
    session.add(message1)
    session.add(message2)
    session.add(message3)
    session.add(message4)
    session.add(message5)
    session.add(message6)
    session.add(message7)
    session.add(message8)

    # Commit and close
    session.commit()
    session.close()

if __name__ == '__main__':
    populate_db()
