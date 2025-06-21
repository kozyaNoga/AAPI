from pydantic import BaseModel, Field, EmailStr

class CreateMovie(BaseModel):
    name: str = Field(min_length=2, max_length=100, example="Список Шиндлера")
    primiere: int = Field(example=1993)
    genre_id: int = Field(gt=0, example=1)
    duration: int = Field(example=195)
    rate: float = Field(example=8.9)
    poster_image: str = Field(example="dfdfddf")
    date_added: int = Field(example = 2025)

class CreateGenre(BaseModel):
    name: str = Field(example="Комедия")

class CreateUser(BaseModel):
    role_id: int = Field(example=2)
    username: str = Field(example="Denis123", min_length=3, max_length=60)
    password: str = Field(example="qwerty123", min_length=8, max_length=60)
    email: EmailStr | None = Field(None)

class CreateHall(BaseModel):
    count_of_places: int = Field(example=300)

class CreateSession(BaseModel):
    movie_id: int = Field(example=1)
    hall_id: int = Field(example=1)
    time: int = Field(example=60)
    price: int = Field(example=10)

class CreateTicket(BaseModel):
    user_id: int = Field(example=1)
    movie_id: int = Field(example=1)
    hall_id: int = Field(example=1)
    place: int = Field(example=30)

class CreateComment(BaseModel):
    user_id: int = Field(example=1)
    movie_id: int = Field(example=1)
    text: str = Field(example="10 баллов")
