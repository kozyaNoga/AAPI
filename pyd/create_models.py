from pydantic import BaseModel, Field

class CreateMovie(BaseModel):
    name: str = Field(min_length=2, max_length=100, example="Список Шиндлера")
    primiere: int = Field(example=1993)
    genre_id: int = Field(gt=0, example=1)
    duration: int = Field(example=195)
    rate: float = Field(example=8.9)
    poster_image: str = Field(example="dfdfddf")
    date_added: int = Field(example = 2025)