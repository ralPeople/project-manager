import copy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project_network.modelForms import EdgeForm, EdgeFormTextForm, EdgeFormList
from flask import session
from graph.classes import Graph, Node, EdgeLite, Edge
from graph.build.graphInit import build_graph
from Exceptions.exceptions import InvalidEdgeException, InvalidNodeException, InvalidInputException
from graph.draw.draw import draw_graph

from markupsafe import escape


def escape_html(text):
    return escape(text)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


bp_create_model = Blueprint('bp_create_model', __name__)

@bp_create_model.route('/create_model', methods=['GET', 'POST'])
def create_model():
    form = EdgeFormList()

    if form.is_submitted():
        if form.submit.data and form.validate():
            result, new_html = process_submit(form)
            if result:
                result_html, html = new_html
                if result_html:
                    return render_template("draw.html", new_html=html)
        if form.change.data:
            return redirect(url_for("bp_create_model.create_model_text"))

    return render_template("createModel.html", title='Главная страница', form=form)


@bp_create_model.route('/create_model_text', methods=['GET', 'POST'])
def create_model_text():
    form = EdgeFormTextForm()

    if form.is_submitted():
        if form.change.data:
            return redirect(url_for("bp_create_model.create_model"))
        if form.submit.data and form.validate():
            result, new_html = process_submit_text(form)
            if result:
                result_html, html = new_html
                if result_html:
                    return render_template("draw.html", new_html=html)

    return render_template("createModelText.html", title='Главная страница', form=form)


def process_submit_text(form):
    text = form.text.data
    edge_list = []
    n = 0
    for i, line in enumerate(text.splitlines()):
        try:
            if len(line) == 0:
                raise InvalidInputException(f"Пустая строка с номером {i + 1}")
            ln = line.split()
            print(ln)
            if len(ln) > 4:
                for i in range(4, len(ln)):
                    ln[3] = ln[3] + " " + ln[i]
                while len(ln) > 4:
                    ln.pop()
            print("ДЕБАЖУ", ln)
            if len(ln) < 3:
                raise InvalidInputException(f"В строке с номером {i + 1} слишком мало данных")
            if len(ln) == 3:
                x, y, t = ln
                t = [int(t), ""]
            else:
                x, y, t, name = ln
                t = [int(t), escape_html(name)]
            x = int(x)
            y = int(y)
            edge_list.append(EdgeLite(x, y, t))
            n = max(n, x, y)
        except InvalidInputException as e:
            flash(f"Ошибка ввода данных {e}", "error")
            return False, 0
        except ValueError as e:
            flash(f"Ошибка ввода данных, вы ввели неправильные типы данных!", "error")
            return False, 0
        except Exception as e:
            flash(f"Ошибка: {e}", "error")
            return False, 0
    m = len(edge_list)
    return True, build_model(n, m, edge_list)


def process_submit(form):
    edge_list = []
    n = 0
    for edge_form in form.edges.entries:
        edge_info = {
            'node1': edge_form.node1.data,
            'node2': edge_form.node2.data,
            'time': edge_form.time.data,
            'job_name': edge_form.job_name.data,
        }
        x = int(edge_info['node1'])
        y = int(edge_info['node2'])
        n = max(n, int(x), int(y))
        t = [edge_info['time'], escape_html(edge_info['job_name'])]

        edge_list.append(EdgeLite(x, y, t))

    m = len(edge_list)
    return True, build_model(n, m, edge_list)


def build_model(n, m,edge_list):
    try:
        g = Graph(n, m, edge_list)
        build_graph(g)
        new_html = draw_graph(g)
        # return new_html
        return True, new_html

    except InvalidEdgeException as e:
        flash(e, "error")
        return False, 0
    except InvalidNodeException as e:
        flash(e, "error")
        return False, 0
    except Exception as e:
        flash(f"Непредвиденная ошибка: {e}", "error")
        return False, 0
