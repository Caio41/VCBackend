from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database.models import Usuario, UsuarioCreate, UsuarioPublic
from deps import SessionDep
from service.usuarios_service import create_usuario_with_hashing

router = APIRouter()



@router.get('/')
def get_all_usuarios(db: SessionDep) -> list[UsuarioPublic]:
    return db.exec(select(Usuario)).all()



@router.post('/')
def create_usuario(usuario_data: UsuarioCreate, db: SessionDep) -> UsuarioPublic:
    return create_usuario_with_hashing(usuario_data, db)


# TO-DO: usuario devem poder atualizar seu nome de perfil ?


# testar amanha isso aqui. precisa reiniciar o banco por causa do cascade
@router.delete('/{usuario_id}')
def delete_usuario(usuario_id: int, db: SessionDep) -> dict:
    usuario = db.exec(select(Usuario).filter(Usuario.id == usuario_id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado.')
    
    db.delete(usuario)
    db.commit()
    return {'detail': f'Usuário {usuario_id} deletado com sucesso'}

