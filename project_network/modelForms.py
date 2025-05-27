from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EdgeForm(FlaskForm):
    node1 = IntegerField("Первое событие",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})
    node2 = IntegerField("Второе событие",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})
    time = IntegerField("Длительность",validators=[DataRequired(), NumberRange(min=0, message="Значение должно быть неотрицательным")], render_kw={"size": 1})
    job_name = StringField("Название (можно пустое)")

    class Meta:
        csrf = False  # ⬅️ Это ключ


class EdgeFormList(FlaskForm):
    edges = FieldList(FormField(EdgeForm), min_entries=1)
    submit = SubmitField('Нарисовать сетевую модель')
    change = SubmitField("Способ ввода через текст")



class EdgeFormTextForm(FlaskForm):
    text = TextAreaField("Ввод данных", validators=[DataRequired()])
    submit = SubmitField('Нарисовать сетевую модель')
    change = SubmitField("Способ ввода через формы")

