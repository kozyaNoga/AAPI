from .base_models import *

class SchemaMovie(BaseMovie):
    genre: BaseGenre | None

class SchemaSession(BaseSession):
    movie: BaseMovie | None
    hall: BaseHall | None

class SchemaTicket(BaseTicket):
    user: BaseUser | None
    movie: BaseMovie | None
    hall: BaseHall | None

class SchemaComment(BaseComment):
    user: BaseUser | None
    movie: BaseMovie | None