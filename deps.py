from os import getenv
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from database.models import Usuario, UsuarioPublic
from database.utils import engine
from service.usuarios_service import get_usuario_by_email

load_dotenv()

AUTH_SECRET_KEY = getenv('AUTH_SECRET_KEY')
AUTH_ALGORITHM = getenv('AUTH_ALGORITHM')

def get_session():
    with Session(engine) as session:
        yield session

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Credenciais não validadas, Tente fazer o login novamente.',
    headers={'WWW-Authenticate': 'Bearer'},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_usuario(db: SessionDep, token: str = Depends(oauth2_scheme)) -> Usuario:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        email: str = payload.get('sub')

    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    usuario = get_usuario_by_email(db, email)
    if usuario is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return usuario


CurrentUsuario = Annotated[UsuarioPublic, Depends(get_current_usuario)]