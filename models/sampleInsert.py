from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database_model import Registered_User, Tutor, Topic, Message, Times
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
import random
import os

def populate_db():
    # Load environment variables from .env file
    load_dotenv()

    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")

    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)

    try:
        with Session() as session:
            # Add Registered Users
            users = [
                Registered_User(first_name=f'User{i}', last_name='Doe', email=f'user{i}@example.com')
                for i in range(1, 21)  # Creating 20 users
            ]
            session.add_all(users)

            # Add Topics
            topic_names = ['Math', 'Physics', 'Chemistry', 'Biology', 'English', 
                            'History', 'Geography', 'Art', 'Music', 'Computer Science']
            topics = [Topic(name=name) for name in topic_names]
            session.add_all(topics)

            # Add Times
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            times = [Times(day=day, start_time=f'9:00', end_time=f'10:00') for day in days]
            session.add_all(times)
            profile_picture_links = [
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/jake.jpg',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/jessica.jpg',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp', 
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Aria.jpg',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Mahdi.jpg',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg',
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Barry.webp',  
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/Aria.jpg', 
                'https://awsgroup1media.s3.us-west-1.amazonaws.com/john.jpg'  
            ]
            # Add Tutors
            tutors = [
                Tutor(user=users[i], description=f'Expert in {topic_names[i]}', price=30.0 + i, 
                        average_ratings=4.0 + i%5 * 0.1, classes=topic_names[i], 
                        main_languages='English', prefer_in_person=i%2==0,
                        cv_link=f'https://example.com/cv/tutor{i}.pdf', 
                        profile_picture_link=profile_picture_links[i],
                        times=random.sample(times, random.randint(1, 3)),
                        other_languages='Spanish, French', topics=random.sample(topics, random.randint(2, 4)))
                for i in range(10)
            ]
            session.add_all(tutors)

            # Add Messages
            messages = [
                Message(sender_id=i, receiver_id=i+1, 
                        message_text=f'Message content {i}')
                for i in range(1,19)  # Creating 20 messages
            ]
            session.add_all(messages)

            # Commit the session once all entities are added
            session.commit()
            return 'Database populated successfully'
    except IntegrityError as e:
        if e and 'Duplicate entry' in str(e):
            return f'SQL Error: Did you already populate the database?'
        else:
            return f'SQL Integrity Error: {e}'
    except Exception as e:
        return f'Error: {e}'