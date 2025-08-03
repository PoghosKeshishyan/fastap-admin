from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .. import models
from ..dependencies import get_db_session, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def read_data(request: Request, db: Session = Depends(get_db_session)):
    user = get_current_user(request)
    items = db.query(models.Item).all()

    return templates.TemplateResponse("items/index.html", {
        "request": request, "data": items, "user": user, "title": "Items"
    })


@router.get("/create", response_class=HTMLResponse)
def create_data_page(request: Request):
    user = get_current_user(request)

    return templates.TemplateResponse("items/create.html", {
        "request": request, "title": "Create Item", "user": user
    })


@router.post("/create", response_class=HTMLResponse)
def create_data(
    request: Request,
    title: str = Form(...),
    description: str = Form(),
    db: Session = Depends(get_db_session)
):
    get_current_user(request)
    item = models.Item(title=title, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return RedirectResponse(url="/items", status_code=status.HTTP_302_FOUND)


@router.get("/edit/{id}", response_class=HTMLResponse)
def edit_data_page(request: Request, id: int, db: Session = Depends(get_db_session)):
    user = get_current_user(request)
    item = db.query(models.Item).filter(models.Item.id == id).first()

    if not item:
        return RedirectResponse(url="/items", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("items/update.html", {
        "request": request, "data": item, "title": "Edit Item", "user": user
    })


@router.post("/edit/{id}", response_class=HTMLResponse)
def edit_data(
    request: Request,
    id: int,
    title: str = Form(...),
    description: str = Form(),
    db: Session = Depends(get_db_session)
):
    get_current_user(request)
    item = db.query(models.Item).filter(models.Item.id == id).first()
    item.title = title
    item.description = description
    db.commit()
    return RedirectResponse(url="/items", status_code=status.HTTP_302_FOUND)


@router.get("/remove/{id}")
def remove_data(request: Request, id: int, db: Session = Depends(get_db_session)):
    get_current_user(request)
    item = db.query(models.Item).filter(models.Item.id == id).first()

    if item:
        db.delete(item)
        db.commit()

    return RedirectResponse(url="/items", status_code=status.HTTP_302_FOUND)