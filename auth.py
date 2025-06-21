from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from sqlalchemy.orm import Session
from database import get_db
import models as m
security = HTTPBasic()

def basic_auth(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user_db = db.query(m.User).filter(m.User.username == credentials.username).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    if user_db.password == credentials.password:
        return user_db
    raise HTTPException(401, "Неверный логин или пароль")

class AuthHandler:
    security=HTTPBearer()
    pwd_content=CryptContext(
        schemes=['bcrypt']
    )
    secret=''
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    def verify_password(self, input_password, db_password):
        return self.pwd_context.verify(input_password, db_password)
    def encode_token(self, user_id):
        payload={
            'ext': datetime.datetime.now()+datetime.timedelta(minutes=30),
            'iat': datetime.datetime.now(),
            'user_id': user_id
        }
        return jwt.encode(payload, self.secret, algorithm=['HS256'])
    def decode_token(self, token):
        try:
            payload= jwt.decode(
                token,
                self.secret,
                algorithms=['HS256']
            )
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Просрочка")
        except jwt.InvalidTokenError:
            raise HTTPException(401, )
    
