from datetime import datetime, timedelta, timezone
from os import getenv
from dotenv import load_dotenv
from sqlmodel import Session, select
from database.models import Usuario, UsuarioCreate, UsuarioPublic
from passlib.context import CryptContext
import jwt

load_dotenv()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# criados manualmente no env
AUTH_SECRET_KEY = getenv('AUTH_SECRET_KEY')
AUTH_ALGORITHM = getenv('AUTH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_usuario_with_hashing(usuario_data: UsuarioCreate, db: Session) -> UsuarioPublic:
    usuario = Usuario.model_validate(
        usuario_data,
        update={
            'senha_hash': bcrypt_context.hash(usuario_data.senha)
        }
    )

    db.add(usuario)
    db.commit()
    return usuario



def authenticate_user(email: str, senha: str, db: Session):
    usuario = db.exec(select(Usuario).filter(Usuario.email==email)).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha_hash):
        return False
    return usuario


def create_access_token(email: str, usuario_id: int):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    
    encode = {
        'sub': email,
        'id': usuario_id,
        'exp': expire
    }

    return jwt.encode(encode, AUTH_SECRET_KEY, AUTH_ALGORITHM)