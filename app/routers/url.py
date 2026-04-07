from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from app.db.deps import get_db
from app.core.utils import encode_base62


router = APIRouter()

BASE_URL = "http://localhost:8000"

@router.post("/shorten", response_model=URLResponse)
def shorten_url(data: URLCreate, db: Session = Depends(get_db)):
    new_url = URL(original_url=str(data.original_url))
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    short_code = encode_base62(new_url.id)
    
    new_url.short_code = short_code
    db.commit()

    return {
        "short_url": f"{BASE_URL}/{short_code}"
    }





