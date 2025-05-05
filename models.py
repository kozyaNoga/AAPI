from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    primiere = Column(Integer)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    duration = Column(Integer)
    rate = Column(Float)
    poster_image = Column(String(255), nullable=True)
    date_added = Column(Integer)

    genre = relationship("Genre", backref="movies")

class Genre(Base): #1
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(), server_default=func.now())