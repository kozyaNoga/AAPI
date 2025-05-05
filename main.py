from fastapi import FastAPI, HTTPException, Depends, UploadFile
import models
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import shutil
from fastapi.staticfiles import StaticFiles
from pyd.base_models import BaseUser
from pyd.create_models import CreateUser
from auth import basic_auth

app = FastAPI()

@app.get("/movies", response_model=list[pyd.BaseMovie])
def get_all_movies(db: Session = Depends(get_db)):
    movies = db.query(m.Movie).all()
    return movies

@app.get("/movie/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    return movie

@app.post("/movie")
def create_movie(movie: pyd.CreateMovie, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    movie_db=db.query(m.Movie).filter(
        m.Movie.name == movie.name, 
        m.Movie.primiere == movie.primiere,
        m.Movie.genre_id == movie.genre_id,
        m.Movie.duration == movie.duration,
        m.Movie.rate == movie.rate,
        m.Movie.poster_image == movie.poster_image,
        m.Movie.date_added == movie.date_added,
    ).first()

    genre_db = db.query(m.Genre).filter(m.Genre.id == movie.genre_id).first()
    if not genre_db:
        raise HTTPException(400, "Нет такой категории")
    if movie_db:
        raise HTTPException(400, "Такой фильм уже есть")
    movie_db = m.Movie()
    movie_db.name = movie.name 
    movie_db.primiere = movie.primiere
    movie_db.genre = genre_db
    movie_db.duration = movie.duration
    movie_db.rate = movie.rate
    movie_db.poster_image = movie.poster_image
    movie_db.date_added = movie.date_added

    db.add(movie_db)
    db.commit()
    return movie_db

@app.delete("/movie/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    movie = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    db.delete(movie)
    db.commit()
    return {"msg": "Фильм удален"}

@app.post("/movie/poster_image/{movie_id}", response_model=pyd.SchemaMovie)
def upload_image(movie_id: int, image: UploadFile, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    movie_db = (
        db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    )
    if not movie_db:
        raise HTTPException(404)
    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Неверный тип данных")
    with open(f"files/{image.filename}", "wb") as f:
        shutil.copyfileobj(image.file, f)
    movie_db.poster_image = f"files/{image.filename}"
    db.commit()
    return movie_db

@app.post("/user", response_model=BaseUser)
def user_reg(create_user: CreateUser, db: Session = Depends(get_db)):
    user_db = db.query(m.User).filter(m.User.username == create_user.username).first()
    if user_db:
        raise HTTPException(400, "Логин занят")
    user_db = m.User()
    user_db.username = create_user.username
    user_db.password = create_user.password
    user_db.email = create_user.email
    db.add(user_db)
    db.commit()
    return user_db

@app.get("/test")
def get_test(user: m.User = Depends(basic_auth)):
    return {"r": 2}