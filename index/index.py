from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from index.indexForms import MainForm


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


bp_index = Blueprint('bp_index', __name__)

@bp_index.route('/index', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.is_submitted():
        if form.model.data:
            return redirect(url_for('bp_create_model.create_model'))
        if form.gantt.data:
            return redirect(url_for("bp_create_gantt.create_gantt"))
        #if form.gantt.data:


    return render_template("index.html", title='Главная страница', form=form)