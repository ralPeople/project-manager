from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    text = StringField('Вариант ответа', validators=[DataRequired()])
    correct = BooleanField('Правильный ответ?')
    delete = SubmitField("Удалить")


class QuestionForm(FlaskForm):
    question_text = TextAreaField('Вопрос', validators=[DataRequired()])
    AnswerList = FieldList(FormField(AnswerForm))
    add = SubmitField('Добавить вариант ответа')
    delete = SubmitField('Удалить вопрос')


class QuizForm(FlaskForm):
    title = StringField('Название теста', validators=[DataRequired()])
    QuestionList = FieldList(FormField(QuestionForm))
    create_question = SubmitField('Добавить вопрос')
    submit_quiz = SubmitField('Создать тест')