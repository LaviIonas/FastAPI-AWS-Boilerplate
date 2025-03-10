from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI AWS-powered API!"}

@app.post("/data/", response_model=schemas.DataResponse)
def create_data(data: schemas.DataCreate, db: Session = Depends(get_db)):
    db_data = models.Data(value=data.value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/data/")
def get_all_data(db: Session = Depends(get_db)):
    return db.query(models.Data).all()
