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

class Session(Base): 
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    time = Column(Integer)
    price = Column(Integer)

    movie = relationship("Movie", backref="sessions")
    hall = relationship("Hall", backref="sessions")

class Hall(Base): 
    __tablename__ = "halls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    count_of_places = Column(Integer)

class Ticket(Base): 
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    hall_id = Column(Integer, ForeignKey("halls.id"))
    place = Column(Integer)

    user = relationship("User", backref="tickets")
    movie = relationship("Movie", backref="tickets")
    hall = relationship("Hall", backref="tickets")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    username = Column(String(60), unique=False, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    role = relationship("Role", backref="roles")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    text = Column(String(), nullable=False)

    user = relationship("User", backref="users")
    movie = relationship("Movie", backref="movies")
