from fastapi import APIRouter, File, UploadFile
from service.videos_service import upload_file, list_files, get_video_with_key

router = APIRouter()

@router.get('')
def get_all_videos():
    response = list_files()
    return response


@router.post('')
async def upload_video(file: UploadFile = File(...)):
    await upload_file(file)
    return f'file: {file.filename}.'



@router.get('/{video_key}')
def get_video(key: str):
    return get_video_with_key(key)
    
