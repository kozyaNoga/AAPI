from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import json, random

app = FastAPI()

@app.get("/about")
def about():
    return json.loads(
        """{
                "name": "Егор",
                "last_name": "Ксенофонтов",
                "groupe": "323901"

            }""")

@app.get("/rnd")
def rnd():
    return random.randint(1, 10)

@app.post("/t_square" )
def t_square(a: int, b: int, c: int):
    if a <= 0 or b <= 0 or c <= 0:
        raise HTTPException(404, "Одна из сторон меньше нуля")
    if a >= b + c or c >= b + a or b >= a + c:
        raise HTTPException(404, "Такого треугольника не существует")
    p = (a + b + c)/2
    s = (p*(p-a)*(p-b)*(p-c))**(1/2)
    return s

@app.get("/product", response_model=list[pyd.BaseProduct])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(m.Product).all()
    return products

@app.get("/student", response_model=list[pyd.BaseStudent])
def get_all_students(db: Session = Depends(get_db)):
    student = db.query(m.Student).all()
    return student

@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    return product

@app.post("/product")
def create_product(product: pyd.CreateProduct, db: Session = Depends(get_db)):
    product_db=db.query(m.Product).filter(m.Product.name == product.name).first()
    if product_db:
        raise HTTPException(400, "Такой товар уже есть")
    product_db = m.Product()
    product_db.name = product.name

    db.add(product_db)
    db.commit()
    return product_db

@app.get("/student/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(m.Student).filter(m.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Студент не найден")
    return student

@app.post("/student")
def create_student(student: pyd.CreateStudent, db: Session = Depends(get_db)):
    student_db=db.query(m.Student).filter(
        m.Student.name == student.name, 
        m.Student.last_name == student.last_name,
        m.Student.age == student.age).first()
    if student_db:
        raise HTTPException(400, "Такой студент уже есть")
    student_db = m.Student()
    student_db.name = student.name

    db.add(student_db)
    db.commit()
    return student_db

@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(m.Product).filter(m.Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    db.delete(product)
    db.commit()
    return {"msg": "Товар удален"}

@app.delete("/student/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(m.Student).filter(m.Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Студент не найден")
    db.delete(student)
    db.commit()
    return {"msg": "Студент удален"}

@app.get("/products", response_model=List[pyd.SchemaProduct])
def get_all_products(db:Session=Depends(get_db)):
    products = db.query(m.Product).all()
    return products