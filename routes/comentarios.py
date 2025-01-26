from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.models import Comentario, ComentarioCreate, ComentarioPublic, Video
from database.utils import SessionDep


router = APIRouter()


@router.get('/{video_id}')
def get_all_comments_from_video(video_id: int, db: SessionDep) -> list[ComentarioPublic]:
    video = db.exec(select(Video).filter(Video.id == video_id)).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video não encontrado")
    
    statement = select(Comentario).filter(Comentario.video_id == video.id)
    return db.exec(statement).all()



@router.post('/')
def add_comment(comment_data: ComentarioCreate, db: SessionDep) -> ComentarioPublic:
    comment = Comentario.model_validate(comment_data)
    
    db.add(comment)
    db.commit()
    
    return comment


# adicionar ediçao de comentario dps


@router.delete('/')
def delete_comment(comment_id: int, db: SessionDep):
    statement = select(Comentario).filter(Comentario.id == comment_id)
    comment = db.exec(statement).first()

    if not comment:
        raise HTTPException(status_code=404, detail='Comentário não encontrado')
    
    db.delete(comment)
    db.commit()

    return f'Comentário com ID: {comment_id} deletado com sucesso!'