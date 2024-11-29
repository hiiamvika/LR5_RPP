from . import db #импорт объекта db '.' указывает на то, что db импортируется из того же пакета (или модуля), где находится models.py.
from flask_login import UserMixin 

class users(db.Model, UserMixin): #создаем таблицу users, которая может использовать функции UserMixin
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(120), nullable=False)