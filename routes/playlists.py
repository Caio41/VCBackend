from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.models import Playlist, PlaylistCreate, PlaylistPublic, PlaylistUpdate, Usuario, Video
from database.utils import SessionDep

router = APIRouter()

# talvez seja melhor colocar essa nas rotas de usuario ?
@router.get('/usuarios/{usuario_id}')
def get_all_playlists_from_user(usuario_id: int, db: SessionDep) -> list[PlaylistPublic]:
    usuario = db.exec(select(Usuario).filter(Usuario.id == usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    statement = select(Playlist).filter(Playlist.usuario_id == usuario.id)
    return db.exec(statement).all()



@router.get('/{playlist_id}')
def get_playlist(playlist_id: int, db: SessionDep) -> PlaylistPublic:
    statement = select(Playlist).filter(Playlist.id == playlist_id)
    playlist = db.exec(statement).first()

    if not playlist:
        raise HTTPException(status_code=404, detail='Playlist não encontrada')
    
    return playlist


@router.post('/')
def add_playlist(playlist_data: PlaylistCreate, db: SessionDep) -> PlaylistPublic:
    playlist = Playlist.model_validate(playlist_data)
    
    db.add(playlist)
    db.commit()

    return playlist


@router.post('/{playlist_id}/add-video/{video_id}')
def add_video_to_playlist(playlist_id: int, video_id: int, db: SessionDep) -> PlaylistPublic:
    playlist = db.exec(select(Playlist).filter(Playlist.id == playlist_id)).first()
    video = db.exec(select(Video).filter(Video.id == video_id)).first()

    if not playlist:
        raise HTTPException(status_code=404, detail='Playlist não encontrada')
    
    if not video:
        raise HTTPException(status_code=404, detail='Video não encontrado')
    
    # Pergunta: deveria dar pra adicionar o mesmo video varias vezes na playlist?

    # insano que funciona assim 
    playlist.videos.append(video)
    db.add(playlist)
    db.commit()

    return playlist



@router.delete('/{playlist_id}/remove-video/{video_id}')
def remove_video_from_playlist(playlist_id: int, video_id: int, db: SessionDep) -> PlaylistPublic:
    playlist = db.exec(select(Playlist).filter(Playlist.id == playlist_id)).first()
    video = db.exec(select(Video).filter(Video.id == video_id)).first()

    if not playlist:
        raise HTTPException(status_code=404, detail='Playlist não encontrada')
    
    if not video:
        raise HTTPException(status_code=404, detail='Video não encontrado')
    
    if video in playlist.videos:
        playlist.videos.remove(video)
        db.add(playlist)
        db.commit()

    else:
        raise HTTPException(status_code=400, detail='Esse video não está na playlist')

    return playlist



@router.put('/{playlist_id}')
def edit_playlist(update_info: PlaylistUpdate, playlist_id: int, db: SessionDep) -> PlaylistPublic:
    playlist = db.exec(select(Playlist).filter(Playlist.id == playlist_id)).first()

    # TO-DO: encontrar um jeito melhor de fazer isso p nao ter que copiar esse codigo mil vezes por arquivo
    if not playlist:
        raise HTTPException(status_code=404, detail='Playlist não encontrada')
    
    playlist.nome = update_info.nome

    db.add(playlist)
    db.commit()
    return playlist



@router.delete('/{playlist_id}')
def delete_playlist(playlist_id: int, db: SessionDep):
    playlist = db.exec(select(Playlist).filter(Playlist.id == playlist_id)).first()

    # TO-DO: encontrar um jeito melhor de fazer isso p nao ter que copiar esse codigo mil vezes por arquivo
    if not playlist:
        raise HTTPException(status_code=404, detail='Playlist não encontrada')
    
    db.delete(playlist)
    db.commit()
    return f'Playlist com ID: {playlist_id} deletada com sucesso!'
