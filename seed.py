from sqlalchemy.orm import Session
from database import engine
import models as m
m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    g1 = m.Genre(name="Драма")
    session.add(g1)

    m1 = m.Movie(
        name = "Валл-и",
        primiere = 2008,
        genre = g1,
        duration = 192,
        rate = 8.2,
        poster_image = "frgrvok",
        date_added = 2008)
    session.add(m1)
    session.commit()
    