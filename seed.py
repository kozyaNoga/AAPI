from sqlalchemy.orm import Session
from database import engine
import models as m
m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    genres = [
        m.Genre(name="drama"),          # Драма
        m.Genre(name="comedy"),         # Комедия
        m.Genre(name="action"),         # Боевик
        m.Genre(name="science fiction"), # Фантастика
        m.Genre(name="horror"),         # Ужасы
        m.Genre(name="animation"),      # Мультфильм
        m.Genre(name="thriller")        # Триллер
    ]
    session.add_all(genres)
    session.commit()

    roles = [
        m.Role(name="admin"),
        m.Role(name="viewer"),
        m.Role(name="cashier")
    ]
    session.add_all(roles)
    session.commit()

    movies = [
        m.Movie(name = "Валл-и", primiere = 2008, genre = genres[3], duration = 192, rate = 8.2, poster_image = "frgrvok", date_added = 2008),
        m.Movie(name="Интерстеллар", primiere=2014, genre=genres[2], duration=169, rate=8.6, poster_image="interstellar.jpg", date_added=2020),
        m.Movie(name="Начало", primiere=2010, genre=genres[5], duration=148, rate=8.7, poster_image="inception.jpg", date_added=2020),
        m.Movie(name="Зелёная миля", primiere=1999, genre=genres[3], duration=189, rate=8.6, poster_image="green-mile.jpg", date_added=2020),
        m.Movie(name="Форрест Гамп", primiere=1994, genre=genres[3], duration=142, rate=8.8, poster_image="forrest-gump.jpg", date_added=2020),
        m.Movie(name="Список Шиндлера", primiere=1993, genre=genres[3], duration=195, rate=8.9, poster_image="schindlers-list.jpg", date_added=2020),
        m.Movie(name="Криминальное чтиво", primiere=1994, genre=genres[1], duration=154, rate=8.9, poster_image="pulp-fiction.jpg", date_added=2020),
        m.Movie(name="Семь", primiere=1995, genre=genres[1], duration=127, rate=8.6, poster_image="seven.jpg", date_added=2020),
        m.Movie(name="Матрица", primiere=1999, genre=genres[3], duration=136, rate=8.7, poster_image="matrix.jpg", date_added=2020),
        m.Movie(name="Гладиатор", primiere=2000, genre=genres[6], duration=155, rate=8.5, poster_image="gladiator.jpg", date_added=2020),
        m.Movie(name="Властелин колец: Братство кольца", primiere=2001, genre=genres[6], duration=178, rate=8.8, poster_image="lord-of-the-rings-fellowship.jpg", date_added=2020),
        m.Movie(name="Титаник", primiere=1997, genre=genres[3], duration=194, rate=7.8, poster_image="titanic.jpg", date_added=2020),
        m.Movie(name="Молчание ягнят", primiere=1991, genre=genres[1], duration=118, rate=8.6, poster_image="silence-of-the-lambs.jpg", date_added=2020),
        m.Movie(name="Темный рыцарь", primiere=2008, genre=genres[4], duration=152, rate=9.0, poster_image="dark-knight.jpg", date_added=2020),
        m.Movie(name="Однажды в Америке", primiere=1984, genre=genres[1], duration=229, rate=8.4, poster_image="once-upon-a-time-in-america.jpg", date_added=2020),
        m.Movie(name="Крепкий орешек", primiere=1988, genre=genres[5], duration=131, rate=8.2, poster_image="die-hard.jpg", date_added=2020),
        m.Movie(name="Терминатор 2: Судный день", primiere=1991, genre=genres[2], duration=137, rate=8.5, poster_image="terminator-2.jpg", date_added=2020),
        m.Movie(name="В погоне за счастьем", primiere=2006, genre=genres[3], duration=117, rate=8.0, poster_image="the-pursuit-of-happyness.jpg", date_added=2020),
        m.Movie(name="Пианист", primiere=2002, genre=genres[3], duration=150, rate=8.5, poster_image="the-pianist.jpg", date_added=2020),
        m.Movie(name="Отступники", primiere=2006, genre=genres[1], duration=151, rate=8.5, poster_image="departed.jpg", date_added=2020),
        m.Movie(name="Человек дождя", primiere=1988, genre=genres[3], duration=133, rate=8.3, poster_image="requiem-for-a-dream.jpg", date_added=2020)
    ]
    session.add_all(movies)
    session.commit()
    
    users = [
        # Админ
        m.User(
            role=roles[0],
            username="AdminAlex",
            password="AdminPass123!",
            email="admin@cinema.ru"
        ),
        # Кассир
        m.User(
            role=roles[2],
            username="CashierMaria",
            password="Cashier456!",
            email="cashier@cinema.ru"
        ),
        # Зрители (9 штук)
        m.User(
            role=roles[1],
            username="Viewer1",
            password="ViewerPass1",
            email="viewer1@mail.ru"
        ),
        m.User(
            role=roles[1],
            username="IvanPetrov",
            password="IvanPass123",
            email="ivan.petrov@mail.ru"
        ),
        m.User(
            role=roles[1],
            username="ElenaSidorova",
            password="ElenaPass456",
            email="elena.sidorova@yandex.ru"
        ),
        m.User(
            role=roles[1],
            username="DmitrySmirnov",
            password="DmitryPass789",
            email="dmitry.smirnov@gmail.com"
        ),
        m.User(
            role=roles[1],
            username="OlgaKuznetsova",
            password="OlgaPass321",
            email="olga.kuznetsova@mail.ru"
        ),
        m.User(
            role=roles[1],
            username="SergeyVolkov",
            password="SergeyPass654",
            email="sergey.volkov@yandex.ru"
        ),
        m.User(
            role=roles[1],
            username="AnnaFedorova",
            password="AnnaPass987",
            email="anna.fedorova@gmail.com"
        ),
        m.User(
            role=roles[1],
            username="AlexeyMorozov",
            password="AlexeyPass135",
            email="alexey.morozov@mail.ru"
        ),
        m.User(
            role=roles[1],
            username="NataliaIvanova",
            password="NataliaPass246",
            email="natalia.ivanova@yandex.ru"
        ),
        m.User(
            role=roles[1],
            username="PavelSokolov",
            password="PavelPass579",
            email="pavel.sokolov@gmail.com"
        )
    ]
    session.add_all(users)
    session.commit()

    halls = [
        m.Hall(count_of_places=100),
        m.Hall(count_of_places=100),
    ]
    session.add_all(halls)
    session.commit()

    tickets = []
    for i in range(10):
        ticket = m.Ticket(
            user=users[i % len(users)],
            movie=movies[i % len(movies)],
            hall=halls[i % len(halls)],
            place=(i + 1) * 10
        )
        tickets.append(ticket)
    session.add_all(tickets)
    session.commit()

    sessions = []
    for i in range(10):
        session_obj = m.Session(
            movie=movies[i % len(movies)],
            hall=halls[i % len(halls)],
            time=i*60+60,
            price=50+i
        )
        sessions.append(session_obj)

    session.add_all(sessions)
    session.commit()

    comments = [
        m.Comment(user=users[3], movie=movies[0], text="Фильм огонь!"),
        m.Comment(user=users[5], movie=movies[1], text="Неплохое кино, рекомендую."),
        m.Comment(user=users[7], movie=movies[2], text="Сюжет захватывающий, смотрел на одном дыхании."),
        m.Comment(user=users[3], movie=movies[3], text="Мощный финал, не ожидал такого поворота!"),
        m.Comment(user=users[4], movie=movies[4], text="Отличная игра актеров, особенно главного героя."),
        m.Comment(user=users[5], movie=movies[5], text="Посмотрел с удовольствием, советую друзьям."),
        m.Comment(user=users[6], movie=movies[6], text="Графика впечатляет, спецэффекты на высоте."),
        m.Comment(user=users[7], movie=movies[7], text="Много смешных моментов, хорошее настроение обеспечено."),
        m.Comment(user=users[8], movie=movies[8], text="Занятная история, понравился саундтрек."),
        m.Comment(user=users[9], movie=movies[9], text="Эмоционально сильное кино, надолго останется в памяти."),
        m.Comment(user=users[3], movie=movies[10], text="Приличный сюжет, хорошая постановка."),
        m.Comment(user=users[6], movie=movies[11], text="Довольно увлекательное зрелище, приятно провести вечер."),
        m.Comment(user=users[2], movie=movies[12], text="Фильму однозначно ставлю лайк, понравится многим."),
        m.Comment(user=users[3], movie=movies[13], text="Картинка красивая, смотреть одно удовольствие."),
        m.Comment(user=users[4], movie=movies[14], text="Интересный сценарий, интрига держит до конца."),
        m.Comment(user=users[5], movie=movies[15], text="Насыщенный экшен, держался в напряжении весь просмотр."),
        m.Comment(user=users[6], movie=movies[16], text="Смело заявляю, это лучший фильм сезона."),
        m.Comment(user=users[7], movie=movies[17], text="Хотелось бы больше таких картин, понравилось!"),
        m.Comment(user=users[8], movie=movies[18], text="Получил массу удовольствия, время пролетело незаметно."),
        m.Comment(user=users[5], movie=movies[19], text="Зацепило сразу же, смотрится легко и интересно."),
        m.Comment(user=users[8], movie=movies[20], text="По-настоящему крутой фильм, заслуживающий внимания.")
    ]
    session.add_all(comments)
    session.commit()