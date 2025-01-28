from fastapi import APIRouter

from database.models import UsuarioCreate, UsuarioPublic
from database.utils import SessionDep
from service.usuarios_service import create_usuario_with_hashing

router = APIRouter()


@router.post('/')
def create_usuario(usuario_data: UsuarioCreate, db: SessionDep) -> UsuarioPublic:
    return create_usuario_with_hashing(usuario_data, db)