from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    text = StringField('Вариант ответа',validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question_text = StringField('Вопрос', validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=2, max_entries=4)
    correct_index = RadioField('Правильный вариант', choices=[], coerce=int)
    submit = SubmitField('Добавить вопрос')

class QuizForm(FlaskForm):
    title = StringField('Название квиза', validators=[DataRequired()])
    submit = SubmitField('Создать квиз')