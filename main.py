from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()
connection_string = "mysql+mysqlconnector://root:Isagi11*@localhost:3306/sqlalchemy"
engine = create_engine(connection_string, echo=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}
