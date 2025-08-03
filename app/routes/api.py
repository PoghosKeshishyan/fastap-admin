from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_db_session

router = APIRouter()


@router.get("/items")
def read_items(db: Session = Depends(get_db_session)):
    items = db.query(models.Item).all()
    return items


@router.get('/sliders')
def read_sliders(request: Request, db: Session = Depends(get_db_session)):
    sliders = db.query(models.Slider).all()
    base_url = str(request.base_url) 
    result = []

    for slider in sliders:
        result.append({
            "id": slider.id,
            "title": slider.title,
            "description": slider.description,
            "image": base_url + "uploads/" + slider.image
        })
        
    return result