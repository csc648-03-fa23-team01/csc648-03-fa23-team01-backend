from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from models.database_model import Registered_User, Tutor, Topic, Message
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
        id="1",
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/jake.jpg'
    )
    user2 = Registered_User(
        id='2',
        first_name='Jane',
        last_name='Doe',
        email='jane.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/jessica.jpg'

    )
    user3 = Registered_User(
        id='3',
        first_name='joe',
        last_name='jo',
        email='joe.jo@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp'

    )
    user4 = Registered_User(
        id='4',
        first_name='bill',
        last_name='Doe',
        email='billy.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp'

    )
    user5 = Registered_User(
        id='5',
        first_name='nasd',
        last_name='Doe',
        email='asd.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Aria.jpg'
    )
    user6 = Registered_User(
        id='6',
        first_name='John',
        last_name='asd',
        email='johfsdfdsn.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Mahdi.jpg'
    )
    user7 = Registered_User(
        id='7',
        first_name='asff',
        last_name='Doe',
        email='sdgg.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg'
    )
    user8 = Registered_User(
        id='8',
        first_name='jhjk',
        last_name='Doe',
        email='jhjk.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp'
    )
    user9 = Registered_User(
        id='9',
        first_name='asdasdfsd',
        last_name='Doe',
        email='asdasdfsd.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/Aria.jpg'
    )
    user10 = Registered_User(
        id='10',
        first_name='jkhygui',
        last_name='Doe',
        email='jkhygui.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg'
    )
    user11 = Registered_User(
        id='11',
        first_name='david',
        last_name='Doe',
        email='david.doe@example.com',
        password='password123',
        profile_picture_link='https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg'
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
    session.add(user11)
     # Adding Topics
    topic1 = Topic(name='Math')
    topic2 = Topic(name='Physics')
    topic3 = Topic(name='Science')
    topic4 = Topic(name='Reading')
    topic5 = Topic(name='English')
    topic6 = Topic(name='Spanish')
    topic7 = Topic(name='umm')
    topic8 = Topic(name='yes')
    session.commit()
    session.add(topic1)
    session.add(topic2)
    session.add(topic3)
    session.add(topic4)
    session.add(topic5)
    session.add(topic6)
    session.add(topic7)
    session.add(topic8)
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
        other_languages='Spanish, French',
        topics = [topic1, topic2]
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
        other_languages='German',
        topics = [topic2, topic3]
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
        other_languages='Italian, Spanish',
        topics = [topic3, topic4]
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
        other_languages='French',
        topics = [topic1, topic3]
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
        other_languages='Spanish, German',
        topics = [topic3, topic4,topic5]
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
        other_languages='French, Spanish',
        topics = [topic5, topic6]
    )
    tutor7 = Tutor(
        user=user7,
        description='English Literature Enthusiast',
        price=25.0,
        average_ratings=4.3,
        classes='British Literature, American Literature',
        times_available='Tue, Thu: 10am-3pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor6.pdf',
        other_languages='French, Spanish',
        topics = [topic2, topic7]
    )
    tutor8 = Tutor(
        user=user8,
         description='Biology Expert',
        price=28.0,
        average_ratings=4.6,
        classes='Cell Biology, Genetics',
        times_available='Mon, Wed, Fri: 8am-12pm',
        main_languages='English',
        prefer_in_person=False,
        cv_link='https://example.com/cv/tutor4.pdf',
        other_languages='French',
        topics = [topic1, topic3,topic5,topic6,topic7]
    )
    tutor9 = Tutor(
        user=user9,
        description='Chemistry Guru',
        price=40.0,
        average_ratings=4.8,
        classes='Organic Chemistry, Inorganic Chemistry',
        times_available='Tue-Thu: 10am-6pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor3.pdf',
        other_languages='Italian, Spanish',
        topics=[topic6, topic2, topic7, topic4, topic5]
    )
    tutor10 = Tutor(
        user=user10,
          description='Experienced Math Tutor',
        price=30.0,
        average_ratings=4.5,
        classes='Algebra, Geometry, Calculus',
        times_available='Mon-Fri: 9am-5pm',
        main_languages='English',
        prefer_in_person=True,
        cv_link='https://example.com/cv/tutor1.pdf',
        other_languages='Spanish, French',
        topics = [topic7]
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
