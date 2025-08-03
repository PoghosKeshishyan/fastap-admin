from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .. import auth, models
from ..dependencies import get_db_session


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get('/register', response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse('users/register.html', {
        'request': request, 'error': None, 'title': 'Register'
    })


@router.post('/register', response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db_session)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        return templates.TemplateResponse('users/register.html', {
            'request': request, 
            'title': 'Register',
            'username': username,
            'password': password,
            'error': 'Username already exists.',
        })
    
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    request.session['user'] = new_user.username
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


@router.get('/login', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('users/login.html', {
        'request': request, 'error': None, 'title': 'Login'
    })


@router.post('/login', response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db_session)
):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not auth.verify_password(password, user.password):
        return templates.TemplateResponse('users/login.html', {
            'request': request,
            'title': 'Login',
            'username': username,
            'password': password,
            'error': 'Invalid credentials.',
        })
    
    request.session['user'] = user.username
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


@router.get('/logout')
def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)