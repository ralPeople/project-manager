from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_logic import User


auth_logout = Blueprint('auth_logout', __name__)


@auth_logout.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect(url_for('index'))
