from fastapi import FastAPI
from alchemical import Alchemical
from models.database_model import Registered_User, Tutor, Message
from models.sampleInsert import populate_db
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
db = Alchemical(os.environ["DATABASE_URL"])

@app.get("/")
async def root():

    return {"message": "Hello World"}

@app.get("/test")
async def test():
    print(env_values.get("DATABASE_URL"))
    # populate_db()
    return{"message":"yer"}
#sample query
#select tutors with user_id = 1

# if __name__ == '__main__':

#     with db.Session() as session:
#         tutors = Tutor(user_id=1)
#         query = select(Tutor)
#         for todo in session.scalars(query):
#             print(todo.__dict__)
