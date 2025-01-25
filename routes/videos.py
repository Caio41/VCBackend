from fastapi import APIRouter, File, Form, UploadFile
from database.models import Video, VideoPublic
from service.videos_service import upload_file, list_files, get_video_with_key
from database.utils import SessionDep

router = APIRouter()


@router.get("/")
def get_all_videos():
    response = list_files()
    return response


@router.post("/")
async def upload_video(
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

    return video


@router.get("/{video_key}")
def get_video(key: str):
    return get_video_with_key(key)
