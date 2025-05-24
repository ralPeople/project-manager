from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from db_logic import User, db


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_check = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


auth_register = Blueprint('auth_register', __name__)


@auth_register.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f"Вы уже вошли в акаунт, {current_user.login}")
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        input_login = form.username.data
        input_password = form.password.data
        input_password_check = form.password_check.data

        if(not input_password == input_password_check):
            flash('Пароли не совпадают!', 'error')
            return render_template("register.html", title='Регистрация', form=form)
        user = User.query.filter_by(login=input_login).first()
        if (user):
            flash('Данный пользователь уже существует!', 'error')
            return render_template("register.html", title='Регистрация', form=form)

        success = False
        try:
            user = User(input_login, input_password)
            db.session.add(user)
            db.session.commit()
            flash(f"Успешная регистрация пользователя {input_login}, теперь войдите в аккаунт")
            success = True
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        if(success):
            return redirect(url_for('auth_login.login'))


    return render_template("register.html", title='Регистрация', form=form)