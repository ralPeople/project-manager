from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_logic import User
from config.const import FLASH_ERROR


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


auth_login = Blueprint('auth_login', __name__)


@auth_login.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Вы уже вошли в акаунт, {current_user.login}")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.is_submitted():
        print('Нажата кнопка!')
        if form.submit_login.data and form.validate_on_submit():
            print('Нажата кнопка ВОЙТИ!')
            input_login = form.username.data
            input_password = form.password.data

            user = User.query.filter_by(login=input_login).first()
            succes_enter = False

            if(user and user.compare_password(input_password)):
                succes_enter = True

            if(succes_enter):
                flash(f"Успешный вход пользователя {form.username.data}")
                login_user(user)
                return redirect(url_for('index'))

            flash('Неправильный логин или пароль!', FLASH_ERROR)
        if form.submit_register.data:
            print('Нажата кнопка register')
            return redirect(url_for('auth_register.register'))

    return render_template("login.html", title='Авторизация', form=form)