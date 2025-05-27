from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EdgeForm(FlaskForm):
    node1 = StringField("Первое событие",validators=[DataRequired()], render_kw={"size": 1})
    node2 = StringField("Второе событие",validators=[DataRequired()], render_kw={"size": 1})
    time = FloatField("Длительность",validators=[DataRequired(), NumberRange(min=0, message="Значение должно быть неотрицательным")], render_kw={"size": 1})
    job_name = StringField("Название (можно пустое)")

    class Meta:
        csrf = False  # ⬅️ Это ключ


class EdgeFormList(FlaskForm):
    edges = FieldList(FormField(EdgeForm))
    submit = SubmitField('Нарисовать сетевую модель')


class EdgeFormTextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])

