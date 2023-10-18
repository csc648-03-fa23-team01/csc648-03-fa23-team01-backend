from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

if __name__ == '__main__':
    DATABASE_URI = 'mysql+mysqldb://root:password@localhost:3306/test?charset=utf8'
    engine = create_engine(DATABASE_URI, echo=True)  # echo=True will show generated SQL statements
    Base.metadata.create_all(engine)

# Inserting data into Registered_Users
john = Registered_User(First_Name='John', Last_Name='Doe', Email='john.doe@example.com', Password='hashed_password_1', Admin_Status=False, Profile_Picture_Link='http://example.com/profile1.jpg', Verified_Status=True)
jane = Registered_User(First_Name='Jane', Last_Name='Smith', Email='jane.smith@example.com', Password='hashed_password_2', Admin_Status=True)
alice = Registered_User(First_Name='Alice', Last_Name='Johnson', Email='alice.johnson@example.com', Password='hashed_password_3', Admin_Status=False, Profile_Picture_Link='http://example.com/profile3.jpg', Verified_Status=True)

session.add_all([john, jane, alice])
session.commit()

# Inserting data into Tutors
john_tutor = Tutor(User_ID=john.ID, Average_Ratings=4.5, Classes='Math, Physics', Description='Experienced tutor with 5 years of teaching.', Price=30.00, Times_Available='Weekdays 4pm-6pm', Main_Languages='English', Prefer_in_person=True, CV_Link='http://example.com/cv1.pdf', Other_Languages='French, Spanish')
alice_tutor = Tutor(User_ID=alice.ID, Average_Ratings=4.0, Classes='English, Literature', Description='Passionate about languages and literature.', Price=25.00, Times_Available='Weekends 10am-1pm', Main_Languages='English', Other_Languages='German')

session.add_all([john_tutor, alice_tutor])
session.commit()

# Inserting data into Messages
message_1 = Message(Who_Sent=john.ID, Message_Text='Hello, I would like to book a session.', When_Sent=datetime.datetime.now(), Message_ID=1001)
message_2 = Message(Who_Sent=alice.ID, Message_Text='Sure, let\'s schedule a time.', When_Sent=datetime.datetime.now(), Message_ID=1002)

session.add_all([message_1, message_2])
session.commit()

# Closing the session
session.close()
