from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    model = SubmitField('Сетевая модель')
    gantt = SubmitField('Диаграмма Ганта')
