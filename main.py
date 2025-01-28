
from fastapi import FastAPI

from routes import videos, comentarios, playlists, comunidades, usuarios, auth
from database.utils import init_db


app = FastAPI()

app.include_router(videos.router, prefix='/videos', tags=['videos'])
app.include_router(comentarios.router, prefix='/comentarios', tags=['comentarios'])
app.include_router(playlists.router, prefix='/playlists', tags=['playlists'])
app.include_router(comunidades.router, prefix='/comunidades', tags=['comunidades'])
app.include_router(usuarios.router, prefix='/usuarios', tags=['usuarios'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])


@app.on_event('startup')
def on_startup():
    init_db()