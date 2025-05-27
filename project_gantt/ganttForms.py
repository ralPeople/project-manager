from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, RadioField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EdgeForm(FlaskForm):
    node1 = IntegerField("Первое событие",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})
    node2 = IntegerField("Второе событие",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})
    time = FloatField("Длительность",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})
    number = IntegerField("Количество исполнителей",validators=[DataRequired(), NumberRange(min=1, message="Значение должно быть положительным")], render_kw={"size": 1})

    class Meta:
        csrf = False


class EdgeFormList(FlaskForm):
    edges = FieldList(FormField(EdgeForm), min_entries=1)
    submit = SubmitField('Нарисовать диаграмму Ганта')
    change = SubmitField("Способ ввода через текст")



class EdgeFormTextForm(FlaskForm):
    text = TextAreaField("Ввод данных", validators=[DataRequired()])
    submit = SubmitField('Нарисовать диаграмму Ганта')
    change = SubmitField("Способ ввода через формы")

