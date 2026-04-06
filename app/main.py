from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import url


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "URL Shortener API running"}