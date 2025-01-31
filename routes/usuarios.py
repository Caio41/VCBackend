from fastapi import APIRouter, HTTPException
from sqlmodel import select

from database.models import Inscricao, Playlist, PlaylistPublic, Usuario, UsuarioCreate, UsuarioPublic
from deps import SessionDep, CurrentUsuario
from service.usuarios_service import create_usuario_with_hashing

router = APIRouter()


@router.get("/")
def get_all_usuarios(db: SessionDep) -> list[UsuarioPublic]:
    return db.exec(select(Usuario)).all()


# do jeito que ta, so da pra ver os inscritos do seu proprio canal. pensar sobre
@router.get("/inscritos")
def get_all_inscritos(
    db: SessionDep, current_usuario: CurrentUsuario
) -> list[UsuarioPublic]:
    inscritos = db.exec(
        select(Usuario)
        .join(Inscricao, Inscricao.inscrito == Usuario.id)
        .filter(Inscricao.canal == current_usuario.id)
    ).all()
    return inscritos


@router.get("/inscricoes")
def get_all_inscricoes(
    db: SessionDep, current_usuario: CurrentUsuario
) -> list[UsuarioPublic]:
    inscricoes = db.exec(
        select(Usuario)
        .join(Inscricao, Inscricao.canal == Usuario.id)
        .filter(Inscricao.inscrito == current_usuario.id)
    ).all()
    return inscricoes


@router.get('/playlists')
def get_all_playlists_from_user(db: SessionDep, current_usuario: CurrentUsuario) -> list[PlaylistPublic]:
    usuario = db.exec(select(Usuario).filter(Usuario.id == current_usuario.id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    statement = select(Playlist).filter(Playlist.usuario_id == usuario.id)
    return db.exec(statement).all()


@router.post("/inscrever/{canal_id}")
def create_inscricao(
    canal_id: int, db: SessionDep, current_usuario: CurrentUsuario
) -> Inscricao:
    inscricao_ja_existente = db.exec(
        select(Inscricao).filter(
            Inscricao.canal == canal_id, Inscricao.inscrito == current_usuario.id
        )
    ).first()
    if inscricao_ja_existente:
        raise HTTPException(status_code=409, detail='Usuário já inscrito no canal.')

    inscricao = Inscricao(
        canal=canal_id,
        inscrito=current_usuario.id,
    )

    db.add(inscricao)
    db.commit()
    db.refresh(inscricao)
    return inscricao


@router.post("/")
def create_usuario(usuario_data: UsuarioCreate, db: SessionDep) -> UsuarioPublic:
    return create_usuario_with_hashing(usuario_data, db)


# TO-DO: usuario devem poder atualizar seu nome de perfil ?


@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int, db: SessionDep) -> dict:
    usuario = db.exec(select(Usuario).filter(Usuario.id == usuario_id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()
    return {"detail": f"Usuário {usuario_id} deletado com sucesso"}
