from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project_network.modelForms import EdgeForm, EdgeFormTextForm, EdgeFormList
from flask import session
from graph.classes import Graph, Node, EdgeLite, Edge
from graph.build.graphInit import build_graph
from Exceptions.exceptions import InvalidEdgeException, InvalidNodeException
from graph.draw.draw import draw_graph


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


bp_create_model = Blueprint('bp_create_model', __name__)

@bp_create_model.route('/create_model', methods=['GET', 'POST'])
def create_model():
    form = EdgeFormList()

    if form.validate_on_submit():
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
            t = [edge_info['time'], edge_info['job_name']]

            edge_list.append(EdgeLite(x,y,t))

        m = len(edge_list)
        try:
            g = Graph(n, m, edge_list)
            build_graph(g)
            new_html = draw_graph(g)
            return new_html

        except InvalidEdgeException as e:
            flash(e, "error")
        except InvalidNodeException as e:
            flash(e, "error")
        except Exception as e:
            flash(f"Непредвиденная ошибка: {e}", "error")



    return render_template("createModel.html", title='Главная страница', form=form)

