from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import url
from app.routers import url


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(url.router)

@app.get("/")
def root():
    return {"message": "URL Shortener API running"}