
from fastapi import FastAPI

from database.utils import init_db


app = FastAPI()


@app.on_event('startup')
def on_startup():
    init_db()