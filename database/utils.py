from os import getenv
from typing import Annotated
from dotenv import load_dotenv
import database.models  # noqa: F401

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

DATABASE_URL = getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
# se quiser ver os logs do banco so colocar isso como parametro no crate_engine -> echo=True

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]