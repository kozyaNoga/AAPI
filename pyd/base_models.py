from pydantic import BaseModel, Field

class BaseGenre(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(example="Драма")

class BaseMovie(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100, example="Список Шиндлера")
    primiere: int = Field(example=1993)
    #genre: int = Field(gt=0, example=1)
    duration: int=Field(example=195)
    rate: float=Field(gt=0, example=8.9)
    poster_image: str | None
    date_added: int = Field(example = 2025)
