from datetime import date, datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Inscricao(SQLModel, table=True):
    __tablename__ = "inscricao"

    inscrito: int | None = Field(
        foreign_key="usuario.id", primary_key=True, ondelete="CASCADE"
    )
    canal: int | None = Field(
        foreign_key="usuario.id", primary_key=True, ondelete="CASCADE"
    )

    # mesma logica de following - followed


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Usuario
class UsuarioComunidade(SQLModel, table=True):
    __tablename__ = "usuario_comunidade"

    usuario: int | None = Field(
        foreign_key="usuario.id", primary_key=True, ondelete="CASCADE"
    )
    comunidade: int | None = Field(
        foreign_key="comunidade.id", primary_key=True, ondelete="CASCADE"
    )


class UsuarioBase(SQLModel):
    nome: str
    # foto: str  #add dps
    email: str


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuario"

    id: int | None = Field(default=None, primary_key=True)
    senha_hash: str | None = None

    videos: list["Video"] = Relationship(back_populates="usuario")
    playlists: list["Playlist"] = Relationship(
        back_populates="usuario", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    comentarios: list["Comentario"] = Relationship(back_populates="usuario")
    notificacoes: list['Notificacao'] = Relationship(back_populates='usuario')

    comunidades: list["Comunidade"] = Relationship(
        link_model=UsuarioComunidade, back_populates="usuarios"
    )
    inscritos: list["Usuario"] = Relationship(
        link_model=Inscricao,
        back_populates="inscricoes",
        sa_relationship_kwargs=dict(
            primaryjoin="Usuario.id==Inscricao.canal",
            secondaryjoin="Usuario.id==Inscricao.inscrito",
        ),
    )
    inscricoes: list["Usuario"] = Relationship(
        link_model=Inscricao,
        back_populates="inscritos",
        sa_relationship_kwargs=dict(
            primaryjoin="Usuario.id==Inscricao.inscrito",
            secondaryjoin="Usuario.id==Inscricao.canal",
        ),
    )


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioPublic(UsuarioBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Comentario
class ComentarioBase(SQLModel):
    conteudo: str


class Comentario(ComentarioBase, table=True):
    __tablename__ = "comentario"

    id: int | None = Field(default=None, primary_key=True)
    video_id: int = Field(foreign_key="video.id")
    usuario_id: int = Field(foreign_key="usuario.id")
    likes: int = Field(default=0)

    video: "Video" = Relationship(back_populates="comentarios")
    usuario: "Usuario" = Relationship(back_populates="comentarios")


class ComentarioCreate(ComentarioBase):
    video_id: int
    usuario_id: int


class ComentarioPublic(ComentarioBase):
    id: int
    likes: int
    video_id: int
    usuario_id: int


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Comunidade
class ComunidadeBase(SQLModel):
    nome: str


class Comunidade(ComunidadeBase, table=True):
    __tablename__ = "comunidade"

    id: int | None = Field(default=None, primary_key=True)

    usuarios: list["Usuario"] = Relationship(
        link_model=UsuarioComunidade, back_populates="comunidades"
    )


class ComunidadeCreate(ComunidadeBase):
    pass


class ComunidadeUpdate(ComunidadeBase):
    pass


class ComunidadePublic(ComunidadeBase):
    id: int
    usuarios: list["Usuario"]


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Notificacao
# Notificacao quando faz upload de video (canal inscrito)
# Notificacao quando dao like no video
# Notificacao quando comentam o video
class NotificacaoBase(SQLModel):
    lida: bool = Field(default=False)
    data: date = Field(default=datetime.now())
    mensagem: str


class Notificacao(NotificacaoBase, table=True):
    __tablename__ = "notificacao"

    id: int | None = Field(default=None, primary_key=True)

    usuario_id: int = Field(foreign_key='usuario.id', ondelete='CASCADE')

    usuario: "Usuario" = Relationship(back_populates="notificacoes")


class NotificacaoPublic(NotificacaoBase):
    usuario_id: int

# -----------------------------------------------------------------------------------------------------------------------------------------------
# Videos


# Many to Many: Playlist - Video
class PlaylistVideos(SQLModel, table=True):
    __tablename__ = "playlist_videos"

    playlist: int | None = Field(
        foreign_key="playlist.id", primary_key=True, ondelete="CASCADE"
    )
    video: int | None = Field(
        foreign_key="video.id", primary_key=True, ondelete="CASCADE"
    )


class VideoBase(SQLModel):
    titulo: str
    descricao: str


#    thumb: str
#    duracao: int

# PENSAR SOBRE LIKE SER UM MODEL 

class Video(VideoBase, table=True):
    __tablename__ = "video"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")

    visualizacoes: int = Field(default=0)
    likes: int = Field(default=0)
    data: date = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    url: str

    usuario: "Usuario" = Relationship(back_populates="videos")

    comentarios: list["Comentario"] = Relationship(back_populates="video")

    playlists: list["Playlist"] = Relationship(
        link_model=PlaylistVideos, back_populates="videos"
    )


# acabei nao usando
class VideoCreate(VideoBase):
    usuario_id: int


class VideoPublic(VideoBase):
    id: int
    url: str


class VideoUpdate(VideoBase):
    pass


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Playlist


class PlaylistBase(SQLModel):
    nome: str


class Playlist(PlaylistBase, table=True):
    __tablename__ = "playlist"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE")

    usuario: Usuario = Relationship(back_populates="playlists")

    videos: list["Video"] = Relationship(
        link_model=PlaylistVideos, back_populates="playlists"
    )


class PlaylistPublic(PlaylistBase):
    id: int
    videos: list["Video"]
    usuario_id: int


class PlaylistCreate(PlaylistBase):
    usuario_id: int


class PlaylistUpdate(PlaylistBase):
    pass


# Video        OK
# Usuario
# Comentario   OK
# Comunidade   OK
# Inscrições
# Notificações
# Playlists   OK

# video É DE UM usuario
# video tem 0 a N comentarios
# comentario é de apenas um video
# comentario é de apenas um usuario
# comentario pode ter 0 a N comentarios
# comunidade tem 0 a N usuarios
# usuario pode estar em 0 a N comunidades
# usuario tem 0 a N inscricoes (funciona como follow?)
# usuario tem de 0 a N notificacoes
# notificacao tem apenas UM video
# usuario pode ter 0 a N videos
# playlists tem 1 a N videos
# um video esta em 0 a N playlists
