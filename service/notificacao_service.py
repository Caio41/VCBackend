from sqlmodel import Session, select
from database.models import Notificacao, Usuario
from deps import SessionDep
from service.usuarios_service import obter_inscritos
from service.constants import BATCH_SIZE


def notificar_usuario(receiver_id: int, from_id: int, tipo: str, db: Session):
    return 0


def notificar_inscritos(canal_id: int, db: Session):
    inscritos = obter_inscritos(canal_id, db)
    canal = db.exec(select(Usuario).filter(Usuario.id == canal_id)).first()
    msg = f'Novo vídeos do canal {canal.nome}!'
    
    for i in range(0, len(inscritos), BATCH_SIZE):
        batch = inscritos[i:i+BATCH_SIZE]
        notificacoes = []
        for usuario in batch:
            notificacoes.append(Notificacao(usuario_id=usuario.id, mensagem=msg))
        db.add_all(notificacoes)
        db.commit()
        
