from fastapi import APIRouter
from sqlmodel import select
from database.models import Notificacao, NotificacaoPublic
from deps import SessionDep

router = APIRouter()

# Rotas apenas para teste.

@router.get('/')
def get_all_notificacoes(db: SessionDep) -> list[NotificacaoPublic]:
    return db.exec(select(Notificacao)).all()


@router.get('/{usuario_id}')
def get_all_notifications_from_user(usuario_id: int, db: SessionDep) -> list[NotificacaoPublic]:
    return db.exec(select(Notificacao).filter(Notificacao.usuario_id == usuario_id)).all()