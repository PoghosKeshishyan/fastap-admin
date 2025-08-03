from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from . import auth, models, database
from .routes import api
from .routes import home
from .routes import media
from .routes import users 
from .routes import items
from .routes import sliders


app = FastAPI(
    title="Travel API",
    description="a REST API using python and sqlite3",
    version="0.0.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.mount('/uploads', StaticFiles(directory='app/uploads'), name='uploads')
app.add_middleware(SessionMiddleware, secret_key=auth.SECRET)
models.Base.metadata.create_all(bind=database.engine)


app.include_router(api.router, prefix="/api", tags=["API List Endpoints"])
app.include_router(home.router, prefix='', tags=['home'])
app.include_router(media.router, prefix='/media', tags=['media'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(items.router, prefix='/items', tags=['items'])
app.include_router(sliders.router, prefix='/sliders', tags=['sliders'])