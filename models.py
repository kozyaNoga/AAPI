from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Product(Base): #N
    __tablename__="products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    #img = Cloumn

    category = relationship("Category", backref="products")

class Student(Base):
    __tablename__="students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)

class Category(Base): #1
    __tablename__="categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)

