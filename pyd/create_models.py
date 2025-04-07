from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str = Field(example="Молоко")

class CreateStudent(BaseModel):
    name: str = Field(example="Имя")
    last_name: str = Field(example="Фамилия") 
    age: int = Field(example=100)   