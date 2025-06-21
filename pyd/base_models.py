from pydantic import BaseModel, Field, EmailStr

class BaseMovie(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100, example="Список Шиндлера")
    primiere: int = Field(example=1993)
    genre_id: int = Field(gt=0, example=1)
    duration: int=Field(example=195)
    rate: float=Field(gt=0, example=8.9)
    poster_image: str | None
    date_added: int = Field(example = 2025)

class BaseGenre(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(example="Драма")

class BaseHall(BaseModel):
    id: int = Field(gt=0)
    count_of_places: int = Field(example=300)

class BaseSession(BaseModel):
    id: int = Field(gt=0)
    movie_id: int = Field(example=1)
    hall_id: int = Field(example=1)
    time: int = Field(example=60)
    price: int = Field(example=10)

class BaseTicket(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(example=1)
    movie_id: int = Field(example=1)
    hall_id: int = Field(example=1)
    place: int = Field(example=32)

class BaseUser(BaseModel):
    id: int = Field(gt=0)
    role_id: int = Field(example=2)
    username: str = Field(example="Denis123")
    email: EmailStr | None = Field(None, example="test@mail.ru")

class BaseComment(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(example=1)
    movie_id: int = Field(example=1)
    text: str = Field(example="10 баллов")