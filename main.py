from fastapi import FastAPI
from models.database_model import Base, engine,db
from models.sampleInsert import populate_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def gen():
    Base.metadata.create_all(engine)

@app.get("/populate")
async def populate():
    populate_db()
    return {"message": "Database populated"}