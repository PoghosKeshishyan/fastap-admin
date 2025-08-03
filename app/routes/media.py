import os, shutil
from typing import List
from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
CURRENT_ROUTE = 'media'
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_class=HTMLResponse)
def read_files(request: Request):
    user = get_current_user(request)

    media = []
    files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
    files.sort(key=lambda x: os.path.getctime(os.path.join(UPLOAD_DIR, x)), reverse=True)

    for f in files:
        ext = f.lower().split('.')[-1]
        if ext in ("png", "jpg", "jpeg", "gif", "bmp", "webp"):
            media.append({"filename": f, "type": "image"})
        elif ext in ("mp4", "webm", "ogg"):
            media.append({"filename": f, "type": "video"})
        else:
            media.append({"filename": f, "type": "other"})

    return templates.TemplateResponse("media/index.html", {
        "request": request,
        "media": media,
        "user": user,
        "CURRENT_ROUTE": CURRENT_ROUTE
    })


@router.post("/upload/", response_class=RedirectResponse)
def upload_files(request: Request, files: List[UploadFile] = File(...)):
    get_current_user(request)

    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
    
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return RedirectResponse("/media", status_code=303)


@router.post("/delete/", response_class=RedirectResponse)
def delete_file(request: Request, filename: str = Form(...)):
    get_current_user(request)
    file_location = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_location):
        os.remove(file_location)
        
    return RedirectResponse("/media", status_code=303)