from fastapi import FastAPI, Depends
from alchemical import Alchemical
from models.database_model import Tutor
from sqlalchemy.orm import Session, sessionmaker
from models.database_model import SessionLocal
app = FastAPI()
db = Alchemical('mysql+mysqldb://root:1234@localhost:3306/tutorial_db?charset=utf8')
class SearchInput(BaseModel):
    text: str
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def searchTutorsTopics(text: str, db: Session):
    return db.query(Tutor).filter(Tutor.classes.contains(text)).all()


@app.post("/search")
async def searchTutors(input: SearchInput, db: Session = Depends(get_db)):
    with db as session:
        tutors = searchTutorsTopics(input.text, session)
        return tutors



