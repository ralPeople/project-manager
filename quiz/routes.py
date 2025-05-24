from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_logic import User
from quiz.quizForms import QuizForm, QuestionForm, AnswerForm
from db_logic import Quiz, Question, Answer, QuizResult, db
from config.const import FLASH_ERROR
import copy

quiz_route = Blueprint('quiz_route', __name__)


@quiz_route.route("/create", methods=['POST', 'GET', 'HEAD'])
@login_required
def create():
    try:
        form = QuizForm(request.form)


        if form.is_submitted():
            print("Кнопка нажата")
            if form.create_question.data: #Добавляю вопрос
                print(f"Добавляю новый вопрос в quiz с номером {quiz.quiz_id} от пользователя {current_user.user_id}")
                form.QuestionList.append_entry()

            questions_to_delete = []
            for i, question_form in enumerate(form.QuestionList):
                if question_form.add.data:              # добавить Ответ
                    question_form.AnswerList.append_entry()

                if (question_form.delete.data):
                    questions_to_delete.append(i)

            for i in questions_to_delete[::]:
                form.QuestionList.entries.pop(i)
            for i, question_form in enumerate(form.QuestionList):
                answers_to_delete = []
                for j in answers_to_delete[::]:
                    question_form.AnswerList.entries.pop(j)

            if form.submit_quiz.data: # Добавить Quiz
                can_submit = True
                if(len(form.QuestionList.entries) == 0):
                    flash("В тесте должен быть хотя бы один вопрос!", FLASH_ERROR)
                    can_submit = False
                else:
                    for i, question_form in enumerate(form.QuestionList):
                        if (len(question_form.AnswerList.entries) < 2):
                            flash(f"В вопросе с номером {i + 1} должно быть хотя бы два варианта ответа!", FLASH_ERROR)
                            can_submit = False
                            break
                        count_correct = 0
                        for j, answer_form in enumerate(question_form.AnswerList):
                            if (answer_form.correct.data):
                                count_correct += 1
                                break
                        if(count_correct == 0):
                            flash(f"В вопросе с номером {i + 1} должен быть хотя бы один правильный вариант!", FLASH_ERROR)
                            break
                    print(can_submit)
                    print(form.validate())
                    if(can_submit and form.validate()):
                        flash(f"Ваш тест <{form.title.data}> успешно создан!")
                        try:
                            quiz = Quiz(user_id=current_user.user_id, title="")
                            db.session().add(quiz)
                            db.session().flush()

                            for i, question_form in enumerate(form.QuestionList):
                                question = Question(quiz_id=quiz.quiz_id, question_text=question_form.question_text.data)
                                db.session().add(question)
                                db.session().flush()
                                for j, answer_form in enumerate(question_form.AnswerList):
                                    answer = Answer(question_id=question.question_id, answer_text=answer_form.text.data, is_correct=answer_form.correct.data)
                                    db.session().add(answer)
                                    db.session().flush()

                            db.session().commit()
                            return redirect(url_for('index'))
                        except Exception as e:
                            print(f"Ошибка при записи в базу данных: {e}")
                            db.session().rollback()


    except Exception as e:
        print(f"Ошибка: {e}")
        db.session().rollback()

    return render_template("quizCreate.html", title='Создание теста', form=form, enumerate=enumerate)
