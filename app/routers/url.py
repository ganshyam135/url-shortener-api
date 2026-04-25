from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from app.db.deps import get_db
from app.core.utils import encode_base62

from app.core.redis import redis_client


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

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session=Depends(get_db)):

    cached_url = redis_client.get(short_code)
    if cached_url:
        print("CACHE HIT")
        return RedirectResponse(url=cached_url)
    
    print("DB HIT")

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    redis_client.set(short_code, url.original_url, ex=3600)
    
    #increment clicks
    url.clicks += 1
    db.commit()

    return RedirectResponse(url=url.original_url)




