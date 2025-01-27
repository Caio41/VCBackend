from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.models import Comunidade, ComunidadeCreate, ComunidadePublic, ComunidadeUpdate
from database.utils import SessionDep

router = APIRouter()


@router.get('/{comunidade_id}')
def get_comunidade(comunidade_id: int, db: SessionDep) -> ComunidadePublic:
    comunidade = db.exec(select(Comunidade).filter(Comunidade.id == comunidade_id)).first()

    if not comunidade:
        raise HTTPException(status_code=404, detail='Comunidade não encontrada')
    
    return comunidade

    
# TO-DO: Quando um usuário criar uma comunidade, automaticamente adicioná-lo nela.
@router.post('/')
def create_comunidade(comunidade_data: ComunidadeCreate, db: SessionDep) -> ComunidadePublic:
    comunidade = Comunidade.model_validate(comunidade_data)
    
    db.add(comunidade)
    db.commit()
    return comunidade


@router.put('/{comunidade_id}')
def update_comunidade(update_info: ComunidadeUpdate, comunidade_id: int,  db: SessionDep) -> ComunidadePublic:
    comunidade = db.exec(select(Comunidade).filter(Comunidade.id == comunidade_id)).first()

    if not comunidade:
        raise HTTPException(status_code=404, detail='Comunidade não encontrada')
    
    comunidade.nome = update_info.nome
    
    db.add(comunidade)
    db.commit() 
    return comunidade


@router.delete('/{comunidade_id}')
def delete_comunidade(comunidade_id: int, db: SessionDep):
    comunidade = db.exec(select(Comunidade).filter(Comunidade.id == comunidade_id)).first()

    if not comunidade:
        raise HTTPException(status_code=404, detail='Comunidade não encontrada')
    
    db.delete(comunidade)
    db.commit()
    return f'Comunidade com ID: {comunidade_id} deletada com sucesso!'