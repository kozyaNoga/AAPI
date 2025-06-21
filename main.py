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
import re
from fastapi import Query

def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.fullmatch(pattern, email))
    
def is_password_strong(password):
    # Минимум 8 символов, есть верхний/нижний регистр, цифра и спецсимвол
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_$])[A-Za-z\d!@#$%^&*_$]{8,}$'
    return bool(re.fullmatch(pattern, password))

app = FastAPI()

# Movies
@app.get("/api/movies", response_model=list[pyd.BaseMovie])
def get_all_movies(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, le=10),
    genre_name: str | None = None,
    min_rating: float | None = None,
    db: Session = Depends(get_db)):

    offset = (page - 1) * limit
    query = db.query(m.Movie)
    if genre_name is not None:
        genre = db.query(m.Genre).filter(m.Genre.name ==  genre_name).first()
        if genre:
            genre_id = genre.id
            query = query.filter(m.Movie.genre_id == genre_id)
        else:
            raise HTTPException(404, "Жанр не найден")
    if min_rating is not None:
        query = query.filter(m.Movie.rate >= min_rating)
    movies = query.offset(offset).limit(limit).all()
    return movies

@app.get("/api/movie/{movie_id}", response_model=pyd.BaseMovie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    return movie

@app.post("/api/movie")
def create_movie(movie: pyd.CreateMovie, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
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

@app.post("/api/movie/{movie_id}")
def update_movie(movie_id: int,
                 name: str | None = None,
                 primiere: int | None = None,
                 genre_name: str | None = None,
                 duration: int | None = None,
                 rate: int | None = None,
                 date_added: int | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    movie_db = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    if not movie_db:
        raise HTTPException(404, "Фильм не найден")

    if name:
        movie_db.name = name 
    if primiere:
        movie_db.primiere = primiere
    if genre_name:
        genre_db = db.query(m.Genre).filter(m.Genre.name == genre_name).first()
        if not genre_db:
            raise HTTPException(400, "Нет такого жанра")
        genre_id = genre_db.id
        movie_db.genre = genre_db
    if duration:
        movie_db.duration = duration
    if rate:
        movie_db.rate = rate
    if date_added:
        movie_db.date_added = date_added

    db.commit()
    return movie_db

@app.delete("/api/movie/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    movie = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(404, "Фильм не найден")
    db.delete(movie)
    db.commit()
    return {"msg": "Фильм удален"}


# Generes
@app.get("/api/genres", response_model=list[pyd.BaseGenre])
def get_all_genres(db: Session = Depends(get_db)):
    genres = db.query(m.Genre).all()
    return genres

@app.get("/api/genre/{genre_id}", response_model=pyd.BaseGenre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(m.Genre).filter(m.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(404, "Жанр не найден")
    return genre

@app.post("/api/genre")
def create_genre(genre: pyd.CreateGenre, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    genre_db=db.query(m.Genre).filter(
        m.Genre.name == genre.name
    ).first()

    genre_db = m.Genre()
    genre_db.name = genre.name 

    db.add(genre_db)
    db.commit()
    return genre_db

@app.post("/api/genre/{genre_id}")
def update_genre(genre_id: int,
                 name: str | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    genre_db = db.query(m.Genre).filter(m.Genre.id == genre_id).first()
    if not genre_db:
        raise HTTPException(404, "Жанр не найден")

    if name:
        genre_db.name = name 

    db.commit()
    return genre_db

@app.delete("/api/genre/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    genre = db.query(m.Genre).filter(m.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(404, "Жанр не найден")
    db.delete(genre)
    db.commit()
    return {"msg": "Жанр удален"}


# Sessions
@app.get("/api/sessions", response_model=list[pyd.BaseSession])
def get_all_sessions(db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    sessions = db.query(m.Session).all()
    return sessions

@app.get("/api/session/{session_id}", response_model=pyd.BaseSession)
def get_session(session_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    
    session = db.query(m.Session).filter(m.Session.id == session_id).first()
    if not session:
        raise HTTPException(404, "Сессия не найден")
    return session

@app.post("/api/session")
def create_session(session: pyd.CreateSession, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    session_db=db.query(m.Session).filter(
        m.Session.movie_id == session.movie_id, 
        m.Session.hall_id == session.hall_id,
        m.Session.time == session.time,
        m.Session.price == session.price
    ).first()

    movie_db = db.query(m.Movie).filter(m.Movie.id == session.movie_id).first()
    if not movie_db:
        raise HTTPException(400, "Такого фильма не существует")
    hall_db = db.query(m.Hall).filter(m.Hall.id == session.hall_id).first()
    if not hall_db:
        raise HTTPException(400, "Такого зала не существует")
    if session_db:
        raise HTTPException(400, "Такая сессия уже существует")
    session_db = m.Session()
    session_db.movie = movie_db 
    session_db.hall = hall_db
    session_db.time = session.time
    session_db.price = session.price

    db.add(session_db)
    db.commit()
    return session_db

@app.post("/api/session/{session_id}")
def update_session(session_id: int,
                 movie_id: int | None = None,
                 hall_id: int | None = None,
                 time: int | None = None,
                 price: int | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    session_db = db.query(m.Session).filter(m.Session.id == session_id).first()
    if not session_db:
        raise HTTPException(404, "Сессия не найдена")

    if movie_id:
        movie_db = db.query(m.Movie).filter(m.Movie.id == movie_id).first()
        if not movie_db:
            raise HTTPException(404, "Фильма с таким ид не сущестыует")
        else:
            session_db.movie = movie_db
    if hall_id:
        hall_db = db.query(m.Hall).filter(m.Hall.id == hall_id).first()
        if not hall_db:
            raise HTTPException(404, "Зала с таким ид не сущестыует")
        else:
            session_db.hall = hall_db
    if time:
        session_db.time = time
    if price:
        session_db.price = price
        

    db.commit()
    return session_db

@app.delete("/api/session/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    
    session = db.query(m.Session).filter(m.Session.id == session_id).first()
    if not session:
        raise HTTPException(404, "Сессия не найдена")
    db.delete(session)
    db.commit()
    return {"msg": "Сессия удалена"}



# Halls
@app.get("/api/halls", response_model=list[pyd.BaseHall])
def get_all_halls(db: Session = Depends(get_db)):
    halls = db.query(m.Hall).all()
    return halls

@app.get("/api/hall/{hall_id}", response_model=pyd.BaseHall)
def get_hall(hall_id: int, db: Session = Depends(get_db)):
    hall = db.query(m.Hall).filter(m.Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(404, "Зал не найден")
    return hall

@app.post("/api/hall")
def create_hall(hall: pyd.CreateHall, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    hall_db=db.query(m.Hall).filter(
        m.Hall.count_of_places == hall.count_of_places, 
    ).first()

    if hall_db:
        raise HTTPException(400, "Такой зал уже есть")
    hall_db = m.Hall()
    hall_db.count_of_places = hall.count_of_places

    db.add(hall_db)
    db.commit()
    return hall_db

@app.post("/api/hall/{hall_id}")
def update_hall(hall_id: int,
                 count_of_places: int | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    hall_db = db.query(m.Hall).filter(m.Hall.id == hall_id).first()
    if not hall_db:
        raise HTTPException(404, "Зал не найден")

    if count_of_places:
        hall_db.count_of_places = count_of_places

    db.commit()
    return hall_db

@app.delete("/api/hall/{hall_id}")
def delete_hall(hall_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    hall = db.query(m.Hall).filter(m.Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(404, "Зал не найден")
    db.delete(hall)
    db.commit()
    return {"msg": "Зал удален"}



# Tickets
@app.get("/api/tickets", response_model=list[pyd.BaseTicket])
def get_all_tickets(db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    tickets = db.query(m.Ticket).all()
    return tickets

@app.get("/api/ticket/{ticket_id}", response_model=pyd.BaseTicket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    ticket = db.query(m.Ticket).filter(m.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Билет не найден")
    return ticket

@app.post("/api/ticket")
def create_ticket(ticket: pyd.CreateTicket, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    ticket_db=db.query(m.Ticket).filter(
        m.Ticket.user_id == ticket.user_id,
        m.Ticket.movie_id == ticket.movie_id,
        m.Ticket.hall_id == ticket.hall_id,
        m.Ticket.place == ticket.place,
    ).first()
    ticket_place_db=db.query(m.Ticket).filter(
        m.Ticket.movie_id == ticket.movie_id,
        m.Ticket.hall_id == ticket.hall_id,
        m.Ticket.place == ticket.place,
    ).first()

    movie_db = db.query(m.Movie).filter(m.Movie.id == ticket.movie_id).first()
    hall_db = db.query(m.Hall).filter(m.Hall.id == ticket.hall_id).first()
    user_db = db.query(m.User).filter(m.User.id == ticket.user_id).first()
    if not movie_db:
        raise HTTPException(400, "Нет такого фильма")
    if not hall_db:
        raise HTTPException(400, "Нет такого зала")
    if not user_db:
        raise HTTPException(400, "Нет такого пользователя")
    if ticket_place_db:
        raise HTTPException(400, "Место зянято")
    if ticket_db:
        raise HTTPException(400, "Такой билет уже существует")
    
    ticket_db = m.Ticket()
    ticket_db.user = user_db 
    ticket_db.hall = hall_db
    ticket_db.movie = movie_db
    if not 1 <= ticket.place <= hall_db.count_of_places:
        raise HTTPException(400, "В зале нет места под таким номером")
    ticket_db.place = ticket.place

    db.add(ticket_db)
    db.commit()
    return ticket_db

@app.post("/api/ticket/{ticket_id}")
def update_ticket(ticket_id: int,
                 user_id: int | None = None,
                 movie_id: int | None = None,
                 hall_id: int | None = None,
                 place: int | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    ticket_db = db.query(m.Ticket).filter(m.Ticket.id == ticket_id).first()
    if not ticket_db:
        raise HTTPException(404, "Билет не найден")

    if user_id:
        user_db = db.query(m.User).filter(m.User.id == user_id).first()
        if not user_db:
            raise HTTPException(404, "Нет пользователя с таким ид")
        ticket_db.user = user_db
    if movie_id:
        movie_db = db.query(m.Movie).filter(m.Movie.id == user_id).first()
        if not movie_db:
            raise HTTPException(404, "Нет фильма с таким ид")
        ticket_db.movie = movie_db
    if hall_id:
        hall_db = db.query(m.Hall).filter(m.Hall.id == hall_id).first()
        if not hall_db:
            raise HTTPException(404, "Нет зала с таким ид")
        ticket_db.hall = hall_db
    if place:
        if not 1 <= place <= hall_db.count_of_places:
            raise HTTPException(400, "В зале нет места под таким номером")
        
        ticket_ocupate_place = db.query(m.Ticket).filter(m.Movie.id == movie_id, m.Hall.id == hall_id, m.Ticket.place == place).first()
        if ticket_ocupate_place:
            raise HTTPException(404, "Место занято")
        ticket_db.place = place

    db.commit()
    return ticket_db

@app.delete("/api/ticket/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1 and user.role_id != 3:
        raise HTTPException(401, "У вас не достаточно прав")
    ticket = db.query(m.Ticket).filter(m.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Билет не найден")
    db.delete(ticket)
    db.commit()
    return {"msg": "Билет удален"}



# Users
@app.post("/api/user", response_model=BaseUser)
def user_create(create_user: CreateUser, db: Session = Depends(get_db)):
    user_db = db.query(m.User).filter(m.User.email == create_user.email).first()
    role_db = db.query(m.Role).filter(m.Role.id == create_user.role_id).first()
    if not role_db:
        raise HTTPException(400, "Такой роли не существует")
    if user_db:
        raise HTTPException(400, "Уже существует пользователь, привязанный к этой почте")
    if not is_valid_email(create_user.email):
        raise HTTPException(400, "Введена не корекктный адрес почты")
    if not is_password_strong(create_user.password):
        raise HTTPException(400, "Пароль слишком легкий")
    
    user_db = m.User()
    user_db.role = role_db
    user_db.username = create_user.username
    user_db.password = create_user.password
    user_db.email = create_user.email
    db.add(user_db)
    db.commit()
    return user_db

@app.post("/api/user/{user_id}")
def update_user(user_id: int,
                 role_id: int | None = None,
                 username: str | None = None,
                 password: str | None = None,
                 email: str | None = None,
                 db: Session = Depends(get_db), 
                 user: m.User = Depends(basic_auth)):
    if user.role_id == 1:
        user_db = db.query(m.User).filter(m.User.id == user_id).first()
        if not user_db:
            raise HTTPException(404, "Пользователь не найден")
        if role_id:
            role_db = db.query(m.Role).filter(m.Role.id == role_id).first()
            user_db.role = role_db
        if username:
            user_db.username = username
        if password:
            if not is_password_strong(password):
                raise HTTPException(400, "Пароль слишком легкий")
            user_db.password = password
        if email:
            user_ocupate_email = db.query(m.User).filter(m.User.email == email, m.User.id != user_id).first()
            if user_ocupate_email:
                raise HTTPException(400, "Уже существут пользователь привязанный к этой почте")
            if not is_valid_email(email):
                raise HTTPException(400, "Введен не корекктный адрес почты")
            user_db.email = email
    elif user.id == user_id:
        user_db = db.query(m.User).filter(m.User.id == user_id).first()
        if role_id:
            role_db = db.query(m.Role).filter(m.Role.id == role_id).first()
            user_db.role = role_db
        if username:
            user_db.username = username
        if password:
            if not is_password_strong(password):
                raise HTTPException(400, "Пароль слишком легкий")
            user_db.password = password
        if email:
            user_ocupate_email = db.query(m.User).filter(m.User.email == email, m.User.id != user_id).first()
            if user_ocupate_email:
                raise HTTPException(400, "Уже существут пользователь привязанный к этой почте")
            if not is_valid_email(email):
                raise HTTPException(400, "Введен не корекктный адрес почты")
            user_db.email = email
    else:
        raise HTTPException(401, "У вас не достаточно прав")

    db.commit()
    return user_db

@app.get("/api/users", response_model=list[pyd.BaseUser])
def get_all_users(db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    users = db.query(m.User).all()
    return users

@app.get("/api/user/{user_id}", response_model=pyd.BaseUser)
def get_user(user_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    user = db.query(m.User).filter(m.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return user

@app.delete("/api/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    if user.role_id != 1:
        raise HTTPException(401, "У вас не достаточно прав")
    user = db.query(m.User).filter(m.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"msg": "Пользователь удален"}


# Comments
@app.get("/api/comments", response_model=list[pyd.BaseComment])
def get_all_comments(page: int = Query(default=1, ge=1),
                     limit: int = Query(default=10, le=10),
                     movie: str | None = None,
                     db: Session = Depends(get_db)
                    ):
    offset = (page - 1) * limit
    query = db.query(m.Comment)
    if movie is not None:
        movie_db = db.query(m.Movie).filter(m.Movie.name == movie).first()
        if movie_db:
            movie_id = movie_db.id
            query = query.filter(m.Comment.movie_id == movie_id)
        else:
            raise HTTPException(404, "Фильм не найден")
    comments = query.offset(offset).limit(limit).all()
    return comments

@app.get("/api/comment/{comment_id}", response_model=pyd.BaseComment)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(m.Comment).filter(m.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "Комментарий не найден")
    return comment

@app.post("/api/comment")
def create_comment(comment: pyd.CreateComment, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    comment_db = m.Comment()
    movie_db = db.query(m.Movie).filter(m.Movie.id == comment.movie_id).first()
    user_db = db.query(m.User).filter(m.User.id == comment.user_id).first()
    if not movie_db:
        raise HTTPException(400, "Нет такого фильма")
    
    comment_db.movie = movie_db
    comment_db.user = user
    comment_db.text = comment.text

    db.add(comment_db)
    db.commit()
    return comment_db

@app.post("/api/comment/{comment_id}")
def update_comment(comment_id: int,
                   text: str,
                   db: Session = Depends(get_db), 
                   user: m.User = Depends(basic_auth)):
    comment_db = db.query(m.Comment).filter(m.Comment.id == comment_id).first()
    if user.id != comment_db.user_id:
        raise HTTPException(401, "У вас не достаточно прав")
    comment_db.text = text
    db.add(comment_db)
    db.commit()
    return comment_db

@app.delete("/api/comment/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
    comment_db = db.query(m.Comment).filter(m.Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(404, "Комментарий не найден")
    if user.role_id != 1 and comment_db.user_id != user.id:
        raise HTTPException(401, "У вас не достаточно прав")
    
    db.delete(comment_db)
    db.commit()
    return {"msg": "Комментарий удален"}


# @app.get("/test")
# def get_test(user: m.User = Depends(basic_auth)):
#     return {"r": 2}

# @app.post('/login')
# def user_auth(db: Session = Depends(get_db)):
    
# @app.post("/movie/poster_image/{movie_id}", response_model=pyd.SchemaMovie)
# def upload_image(movie_id: int, image: UploadFile, db: Session = Depends(get_db), user: m.User = Depends(basic_auth)):
#     movie_db = (
#         db.query(models.Movie).filter(models.Movie.id == movie_id).first()
#     )
#     if not movie_db:
#         raise HTTPException(404)
#     if image.content_type not in ("image/png", "image/jpeg"):
#         raise HTTPException(400, "Неверный тип данных")
#     with open(f"files/{image.filename}", "wb") as f:
#         shutil.copyfileobj(image.file, f)
#     movie_db.poster_image = f"files/{image.filename}"
#     db.commit()
#     return movie_db