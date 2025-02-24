from sqlmodel import select
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from database.models import Video, VideoPublic, VideoUpdate
from service.videos_service import delete_video_from_cloud, upload_file, list_files, get_video_with_key
from service.notificacao_service import notificar_inscritos
from deps import SessionDep

router = APIRouter()


@router.get("/")
def get_all_videos():
    response = list_files()
    # TO-DO: adicionar dados do banco tb na resposta
    return response


@router.post("/")
async def upload_video(
    background_tasks: BackgroundTasks,
    db: SessionDep,
    titulo: str = Form(...),
    descricao: str = Form(...),
    usuario_id: int = Form(...),
    file: UploadFile = File(...),
) -> VideoPublic:
    upload_data = await upload_file(file)
    file_key = upload_data['file_key']

    video = Video(
        titulo=titulo,
        descricao=descricao,
        usuario_id=usuario_id,
        url=file_key,
    )

    db.add(video)
    db.commit()

    background_tasks.add_task(notificar_inscritos, usuario_id, db)
    
    return video


@router.get("/{video_id}")
def get_video(video_id: int, db: SessionDep):
    statement = select(Video).filter(Video.id == video_id)
    video = db.exec(statement).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video não encontrado")

    # TO-DO: adicionar dados do banco tb na resposta
    return get_video_with_key(video.url)



@router.put('/{video_id}')
def edit_video(update_info: VideoUpdate, video_id: int, db: SessionDep) -> VideoPublic:
    statement = select(Video).filter(Video.id == video_id)
    video = db.exec(statement).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video não encontrado")
    
    video.titulo = update_info.titulo
    video.descricao = update_info.descricao

    db.add(video)
    db.commit()

    return video


@router.delete('/{video_id}')
def delete_video(video_id: int, db: SessionDep):
    statement = select(Video).filter(Video.id == video_id)
    video = db.exec(statement).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video não encontrado")

    delete_video_from_cloud(video.url)
    db.delete(video)
    db.commit()

    return f'Video com ID: {video_id} deletado com sucesso!'

