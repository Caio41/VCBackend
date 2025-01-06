from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class Inscricao(SQLModel, table=True):
    __tablename__ = 'inscricao'

    inscrito: int | None = Field(foreign_key='usuario.id', primary_key=True, ondelete='CASCADE')
    canal: int | None = Field(foreign_key='usuario.id', primary_key=True, ondelete='CASCADE')

    # mesma logica de following - followed

# -----------------------------------------------------------------------------------------------------------------------------------------------
# Usuario
class UsuarioComunidade(SQLModel, table=True):
    __tablename__ = 'usuario_comunidade'

    usuario: int | None = Field(foreign_key='usuario.id', primary_key=True, ondelete='CASCADE') 
    comunidade: int | None = Field(foreign_key='comunidade.id', primary_key=True, ondelete='CASCADE')



class UsuarioBase(SQLModel):
    nome: str
    foto: str
    email: str
    senha: str


class Usuario(UsuarioBase, table=True):
    __tablename__ = 'usuario'

    id: int | None = Field(default=None, primary_key=True)

    videos: list['Video'] = Relationship(back_populates='usuario')
    comentarios: list['Comentario'] = Relationship(back_populates='usuario')
    
    comunidades: list['Comunidade'] = Relationship(link_model=UsuarioComunidade, back_populates='usuarios')
    inscritos: list['Usuario'] = Relationship(link_model=Inscricao, back_populates='inscricoes')
    inscricoes: list['Usuario'] = Relationship(link_model=Inscricao, back_populates='inscritos')

# -----------------------------------------------------------------------------------------------------------------------------------------------
# Comentario
class ComentarioBase(SQLModel):
    conteudo: str
    likes: int


class Comentario(ComentarioBase, table=True):
    __tablename__ = 'comentario'

    id: int | None = Field(default=None, primary_key=True)
    video_id = Field(foreign_key='video.id')
    usuario_id = Field(foreign_key='user.id')

    video: 'Video' = Relationship(back_populates='comentarios')
    usuario: 'Usuario' = Relationship(back_populates='comentarios')


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Comunidade
class ComunidadeBase(SQLModel):
    nome: str


class Comunidade(ComunidadeBase, table=True):
    __tablename__ = 'comunidade'

    id: int | None = Field(default=None, primary_key=True)

    usuarios = list['Usuario'] = Relationship(link_model=UsuarioComunidade, back_populates='comunidades')

# -----------------------------------------------------------------------------------------------------------------------------------------------
# Notificacao
# vou ajeitar depois isso aqui
class NotificacoesBase(SQLModel):
    lida: bool 
    data: date


class Notificacao(NotificacoesBase, table=True):
    __tablename__ = 'notificacao'

    id: int | None = Field(default=None, primary_key=True)


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Videos

# Many to Many: Playlist - Video
class PlaylistVideos(SQLModel, table=True):
    __tablename__ = 'playlist_videos'

    playlist: int | None = Field(foreign_key='playlist.id', primary_key=True, ondelete='CASCADE') 
    video: int | None = Field(foreign_key='video.id', primary_key=True, ondelete='CASCADE')



class VideoBase(SQLModel):
    titulo: str
    descricao: str
    thumb: str
    visualizacoes: int
    likes: int
    duracao: int
    data: date
    

class Video(VideoBase, table=True):
    __tablename__ = 'video'

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key='usuario.id')

    usuario: 'Usuario' = Relationship(back_populates='videos')

    comentarios: list['Comentario'] = Relationship(back_populates='video')

    playlists: list['Playlist'] = Relationship(link_model=PlaylistVideos ,back_populates='videos')


# -----------------------------------------------------------------------------------------------------------------------------------------------
# Playlist

class PlaylistBase(SQLModel):
    nome: str 



class Playlist(PlaylistBase, table=True):
    __tablename__ = 'playlist'

    id: int | None = Field(default=None, primary_key=True)

    videos: list['Video'] = Relationship(link_model=PlaylistVideos, back_populates='playlists')






# Video
# Usuario
# Comentario
# Comunidade 
# Inscrições
# Notificações
# Playlists

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
