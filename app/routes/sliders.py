from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .. import models
from ..dependencies import get_db_session, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
CURRENT_ROUTE = 'sliders'


@router.get("/", response_class=HTMLResponse)
def read_data(request: Request, db: Session = Depends(get_db_session)):
    user = get_current_user(request)
    sliders = db.query(models.Slider).all()

    return templates.TemplateResponse("sliders/index.html", {
        "request": request, "data": sliders, "user": user, "title": "Sliders", "CURRENT_ROUTE": CURRENT_ROUTE
    })


@router.get("/create", response_class=HTMLResponse)
def create_data_page(request: Request):
    user = get_current_user(request)

    return templates.TemplateResponse("sliders/create.html", {
        "request": request, "title": "Create Slider", "user": user, "CURRENT_ROUTE": CURRENT_ROUTE
    })


@router.post("/create", response_class=RedirectResponse)
def create_data(
    request: Request,
    title: str = Form(...),
    description: str = Form(),
    image: str = Form(...),
    db: Session = Depends(get_db_session)
):
    get_current_user(request)
    slider = models.Slider(title=title, description=description, image=image)
    db.add(slider)
    db.commit()
    db.refresh(slider)
    return RedirectResponse(url="/sliders", status_code=status.HTTP_302_FOUND)


@router.get("/edit/{id}")
def edit_data_page(request: Request, id: int, db: Session = Depends(get_db_session)):
    user = get_current_user(request)
    slider = db.query(models.Slider).filter(models.Slider.id == id).first()

    if not slider:
        return RedirectResponse(url="/sliders", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("sliders/update.html", {
        "request": request, "data": slider, "title": "Edit Slider", "user": user, "CURRENT_ROUTE": CURRENT_ROUTE
    })


@router.post("/edit/{id}", response_class=RedirectResponse)
def edit_data(
    request: Request,
    id: int,
    title: str = Form(...),
    description: str = Form(),
    image: str = Form(...),
    db: Session = Depends(get_db_session)
):
    get_current_user(request)
    slider = db.query(models.Slider).filter(models.Slider.id == id).first()
    slider.title = title
    slider.description = description
    slider.image = image
    db.commit()
    return RedirectResponse(url="/sliders", status_code=status.HTTP_302_FOUND)


@router.get("/remove/{id}", response_class=RedirectResponse)
def remove_data(request: Request, id: int, db: Session = Depends(get_db_session)):
    get_current_user(request)
    slider = db.query(models.Slider).filter(models.Slider.id == id).first()

    if slider:
        db.delete(slider)
        db.commit()

    return RedirectResponse(url="/sliders", status_code=status.HTTP_302_FOUND)