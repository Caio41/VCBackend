from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from deps import SessionDep
from service.usuarios_service import authenticate_user, create_access_token

router = APIRouter()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


@router.post('/token')
def login_access_token(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = authenticate_user(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos')
    token = create_access_token(usuario.email, usuario.id)
    return {'access_token': token, 'token_type': 'bearer'}




