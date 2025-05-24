from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from db_logic import db
from db_logic import User
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.secret_key = '412741253217312'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Если пришел POST-запрос — обрабатываем форму входа
        login_input = request.form['login']  # Получаем введенный логин из формы
        password_input = request.form['password']  # Получаем введенный пароль из формы
        hash_password = generate_password_hash(password_input)


        # Пытаемся найти пользователя в базе по логину
        user = User.query.filter_by(login=login_input).first()

        # Проверяем, что пользователь найден и пароль совпадает (в реальном приложении — проверять хеш)
        if user and user.password == hash_password:
            flash(f'Добро пожаловать, {user.login}!', 'success')  # Показываем приветственное сообщение
            return redirect(url_for('dashboard'))  # Перенаправляем на страницу дашборда

        flash('Неверный логин или пароль', 'error')  # Ошибка при неверных данных
        return redirect(url_for('login'))  # Возвращаем на страницу входа

    # Если GET-запрос — показываем форму входа
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        print(login)

        # Проверка: существует ли такой пользователь
        existing_user = User.query.filter_by(login=login).first()
        if existing_user:
            flash('Логин уже занят', 'error')
            return redirect(url_for('register'))

        # Хешируем пароль
        hashed_password = generate_password_hash(password)

        # Создаем и сохраняем нового пользователя
        new_user = User(login=login, password=hashed_password)
        db.session.add(new_user)

        db.session.commit()

        flash('Вы успешно зарегистрировались! Теперь войдите.', 'success')
        return redirect(url_for('login'))

    return redirect(url_for('login'))

# Заглушка для страницы пользователя после входа
@app.route('/dashboard')
def dashboard():
    return "Это дашборд пользователя — сюда попадет после входа"

app.run(debug=True)



