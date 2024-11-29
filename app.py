# from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager, login_required, login_user, logout_user
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__) #секретный ключ для приложения Flask

app.secret_key = "123" #является важной частью конфигурации Flask
user_db = "viktoriya_knowledge_base" 
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "knowledge_base2"
password = "1021026"
#URL подключения к базе данных PostgreSQL:
app.config ['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #отключает отслеживание изменений в базе данных (лучше производительность)
db.init_app(app) #связывает SQLAlchemy с приложением Flask, делая db.session (сессия SQLAlchemy) доступной для работы с бд

login_manager = LoginManager() #отвечает за управление аутентификацией пользователей

login_manager.login_view = "login" #какой эндпоинт (маршрут)  должен использоваться для перенаправления неавторизованных пользователей.
login_manager.init_app(app) #инициализирует менеджер логинов, связывая его с приложением Flask
# декоратор, который регистрирует функцию load_users в качестве функции загрузчика пользователей
@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id)) #обращаемся к таблице и просим вернуть id польз или none
@app.route('/')
def base():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def process_login():
    errors = ''

    email_form = request.form.get("email")
    password_form = request.form.get("password")

    my_user = users.query.filter_by(email=email_form).first()
    
    if not (email_form or password_form):
        errors = 'Заполните все поля!'
        print(errors)
        return render_template("login.html", errors=errors)
    else:
        if my_user is not None:
            if check_password_hash(my_user.password,password_form): # функция сравнивает введенный пароль с хешированным паролем,  хранящимся в базе данных.
                login_user(my_user, remember=False) # Если пароль верен,  выполняется авторизация пользователя с помощью login_user
                return redirect("/index")           #remember=False  указывает,  что пользователь не должен оставаться авторизованным после закрытия браузера.
            else:
                errors = 'Неверный пароль!'
                return render_template("login.html", errors=errors)
        else:
            errors = 'Пользователя с такой почтой не существует!'
            return render_template("login.html", errors=errors)

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def process_signup():
    errors = ''

    email_form = request.form.get("email")
    password_form = request.form.get("password")
    name_form = request.form.get("name")

    if not (email_form or password_form or name_form):
        errors = 'Пожалуйста, заполните все поля'
        print(errors)
        return render_template("signup.html", errors=errors)

    isUserExist = users.query.filter_by(email=email_form).first()

    if isUserExist is not None:
        errors = 'Пользователь с такой почтой уже существует'
        return render_template("signup.html", errors=errors)
    
    hashedPswd = generate_password_hash(password_form, method='pbkdf2') #захешировали пароль
    newUser = users(email=email_form, password=hashedPswd,name=name_form) #Создание нового объекта users
    #Добавление нового пользователя в базу данных и сохранение изменений.
    db.session.add(newUser)
    db.session.commit()
    return redirect("/login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')







