
from fastapi import FastAPI

from routes import videos, comentarios, playlists, comunidades
from database.utils import init_db


app = FastAPI()

app.include_router(videos.router, prefix='/videos', tags=['videos'])
app.include_router(comentarios.router, prefix='/comentarios', tags=['comentarios'])
app.include_router(playlists.router, prefix='/playlists', tags=['playlists'])
app.include_router(comunidades.router, prefix='/comunidades', tags=['comunidades'])


@app.on_event('startup')
def on_startup():
    init_db()