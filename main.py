from flask import Flask, render_template, redirect, url_for

from flask_login import LoginManager


from graph.classes import *
from graph.build.graphInit import build_graph
from graph.draw import draw as draw_graph

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.secret_key = '314159265358979323846'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Вы должны быть авторизированы для просмотра данной страницы"
login_manager.login_message_category = 'error'


if __name__ == '__main__':
    print('Hi!')
    edges = []
    edges.append(EdgeLite(1, 2, [10, 'first_edge']))
    edges.append(EdgeLite(2, 3, [15, 'second_edge']))
    edges.append(EdgeLite(1, 3, [25, 'third_edge']))

    n = 3
    m = 3
    g = Graph(n, m, edges)

    build_graph(g)

    print(g.list_of_critical_paths)
    print(g.nodes)

    print('Hi 2')

    draw_graph(g)

    #app.run(debug=True)



