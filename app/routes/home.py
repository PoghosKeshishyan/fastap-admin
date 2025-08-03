from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/',  response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get('user')

    return templates.TemplateResponse('home/index.html', {
        'request': request, 'user': user, 'title': 'Home'
    })