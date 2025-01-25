
from fastapi import FastAPI

from routes import videos
from database.utils import init_db


app = FastAPI()

app.include_router(videos.router, prefix='/videos', tags=['login'])


@app.on_event('startup')
def on_startup():
    init_db()