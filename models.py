from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__="products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)

class Student(Base):
    __tablename__="students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    last_name = Column(String(255), unique=True)
    age = Column(Integer, unique=True)