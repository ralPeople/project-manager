import copy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from project_gantt.ganttForms import EdgeForm, EdgeFormTextForm, EdgeFormList
from flask import session
from graph.classes import Graph, Node, EdgeLite, Edge
from graph.build.graphInit import build_graph
from Exceptions.exceptions import InvalidEdgeException, InvalidNodeException, InvalidInputException
from graph.draw.draw import draw_graph
from graph.build.graphHtmlTable import graph_to_html
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import traceback


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit_login = SubmitField('Войти')
    submit_register = SubmitField('Зарегистрироваться')


bp_create_gantt = Blueprint('bp_create_gantt', __name__)

@bp_create_gantt.route('/create_gantt', methods=['GET', 'POST'])
def create_gantt():
    form = EdgeFormList()

    if form.is_submitted():
        if form.submit.data and form.validate():
            result, graph_table_html, images = process_submit(form)
            img1, img2 = images

            if result:
                return render_template("plot.html", img1=img1, img2=img2, table_html_text=graph_table_html)
        if form.change.data:
            return redirect(url_for("bp_create_gantt.create_gantt_text"))

    return render_template("createGantt.html", title='Главная страница', form=form)


@bp_create_gantt.route('/create_gantt_text', methods=['GET', 'POST'])
def create_gantt_text():
    form = EdgeFormTextForm()

    if form.is_submitted():
        if form.submit.data and form.validate():
            result, graph_table_html, images = process_submit_text(form)
            img1, img2 = images

            if result:
                return render_template("plot.html", img1=img1, img2=img2, table_html_text=graph_table_html)
        if form.change.data:
            return redirect(url_for("bp_create_gantt.create_gantt"))

    return render_template("createGanttText.html", title='Главная страница', form=form)


def process_submit_text(form):
    edge_list = []
    n = 0
    text = form.text.data
    for i, line in enumerate(text.splitlines()):
        try:
            if len(line) == 0:
                raise InvalidInputException(f"Пустая строка с номером {i + 1}")
            ln = line.split()
            print(ln)
            if len(ln) > 4:
                raise InvalidInputException(f"В строке с номером {i + 1} слишком много данных")
            if len(ln) < 4:
                raise InvalidInputException(f"В строке с номером {i + 1} слишком мало данных")
            x, y, t, q = ln
            x = int(x)
            y = int(y)
            t = [int(t), int(q)]
            edge_list.append(EdgeLite(x, y, t))
            n = max(n, x, y)
        except InvalidInputException as e:
            flash(f"Ошибка ввода данных {e}", "error")
        except ValueError as e:
            flash(f"Ошибка ввода данных, вы ввели неправильные типы данных!", "error")
        except Exception as e:
            flash(f"Ошибка: {e}", "error")

    m = len(edge_list)
    result, g = build_model(n, m, edge_list)
    if not result:
        return False, 0

    return True, graph_to_html(g), build_gantt(g)


def process_submit(form):
    edge_list = []
    n = 0
    for edge_form in form.edges.entries:
        edge_info = {
            'node1': edge_form.node1.data,
            'node2': edge_form.node2.data,
            'time': edge_form.time.data,
            'number': edge_form.number.data,
        }
        x = int(edge_info['node1'])
        y = int(edge_info['node2'])
        n = max(n, int(x), int(y))
        t = [int(edge_info['time']), int(edge_info['number'])]

        edge_list.append(EdgeLite(x, y, t))

    m = len(edge_list)
    result, g = build_model(n, m, edge_list)
    if not result:
        return False, 0

    return True, graph_to_html(g), build_gantt(g)


def build_gantt(g):
    segments = []
    work_q = dict()
    for i in range(len(g.edges)):
        x = g.edges[i].x
        y = g.edges[i].y
        t = g.edges[i].t
        work_q[(x, y)] = t[1]
        work_q[(y, x)] = t[1]
    for j in range(1, len(g.nodes) + 1):
        for edge in g.e[j]:
            segments.append((edge.info.Trn, edge.info.Trn + edge.t, work_q[edge.x, edge.y], edge.info.Rc, edge.info.Rp))

    return build_segments_graph(g, segments), build_time_graph(segments)


def build_model(n, m, edge_list):
    try:
        g = Graph(n, m, edge_list)
        build_graph(g)
        # return new_html
        return True, g

    except InvalidEdgeException as e:
        flash(e, "error")
        return False, 0
    except InvalidNodeException as e:
        flash(e, "error")
        return False, 0
    except Exception as e:
        flash(f"Непредвиденная ошибка: {e}", "error")
        return False, 0


def build_segments_graph(g, segments):
    points = []
    for i in range(len(segments)):
        l, r, q, _, __ = segments[i]
        points.append((l, i + 1, q))
        points.append((r, i + 1, q))

    for i in range(len(points) - 1):
        x1, y1, q1 = points[i]
        x2, y2, q2 = points[i + 1]
        if y1 == y2:
            plt.plot([x1, x2], [y1, y1], 'k-')
            plt.plot([x2, x2], [y1, y2], 'k-')
            plt.text((x1 + x2) / 2, y1 + 0.1, str(q1), ha='center', va='bottom', fontsize=10, color='black')
            plt.plot([x1, x1], [y1 - 0.2, y1 + 0.2], 'k-')
            plt.plot([x2, x2], [y1 - 0.2, y1 + 0.2], 'k-')

    plt.yticks([])
    plt.grid(True)

    # Сохраняем изображение в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Кодируем в base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return img_base64


def build_time_graph(segments, name=""):
    dayNumber = dict()
    dayNumber2 = dict()
    max_pos = 0
    points = []
    for l, r, q, *_ in segments:
        for pos in range(l, r):
            dayNumber[pos] = dayNumber.get(pos, 0) + q
            max_pos = max(max_pos, pos)

    for l, r, q, *_ in segments:
        for pos in range(l + 1, r + 1):
            dayNumber2[pos] = dayNumber2.get(pos, 0) + q
            max_pos = max(max_pos, pos)

    for i in range(0, max_pos + 1):
        dayNumber.setdefault(i, 0)
        dayNumber2.setdefault(i, 0)
        if dayNumber[i] > 0:
            points.append((i, dayNumber2[i]))
        if dayNumber2[i] > 0:
            points.append((i, dayNumber[i]))

    # Рисуем граф
    last = -1
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        plt.plot([x1, x2], [y1, y1], 'k-')
        if last != y1:
            plt.text((x1 + x2) / 2, y1 + 0.1, str(y1), ha='center', va='bottom', fontsize=8, color='black')
            last = y1
        plt.plot([x2, x2], [y1, y2], 'k-')

    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.grid(True)

    # Сохраняем граф в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    # Кодируем в base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64