from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_logic import User
from config.const import FLASH_ERROR
from db_logic import Quiz

class AnswerForm(FlaskForm):
    correct = BooleanField('')

bp_pass_quiz = Blueprint('bp_pass_quiz', __name__)


@bp_pass_quiz.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def pass_quiz(quiz_id):
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if(not quiz):
        abort(404)
    questions = quiz.question_list

    for quest in questions:
        print(quest.question_text)

    return render_template("passQuiz.html", title='Авторизация', quiz=quiz, questions=questions)