from pydantic import BaseModel, Field

class BaseProduct(BaseModel):
    id:int=Field(example=1)
    name: str = Field(example="Молоко")

class BaseStudent(BaseModel):
    id:int=Field(example=1)
    name: str = Field(example="Имя")
    last_name: str = Field(example="Фамилия") 
    age: int = Field(example=100)  
