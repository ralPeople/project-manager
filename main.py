from flask import Flask, render_template, redirect, url_for
import os
import secrets

from flask_login import LoginManager


from graph.classes import *
from graph.build.graphInit import build_graph
from graph.draw.draw import draw_graph

from index.index import bp_index
from project_network.createModel import bp_create_model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SECRET_KEY'] = 'твоя_длинная_сложная_строка_для_секрета_один_раз_и_навсегда'


app.register_blueprint(bp_index)
app.register_blueprint(bp_create_model)

@app.route('/')
def base():
    return redirect(url_for('bp_index.index'))

if __name__ == '__main__':
    print('Hi!')
    edges = []
    edges.append(EdgeLite(1, 2, [10, 'first_edge']))
    edges.append(EdgeLite(2, 3, [15, 'second_edge']))
    edges.append(EdgeLite(1, 3, [25, 'third_edge']))

    n = 3
    m = 3
    #g = Graph(n, m, edges)

    #build_graph(g)

    #print(g.list_of_critical_paths)
    #print(g.nodes)

    print('Hi 2')

    #draw_graph(g)

    app.run(debug=True)



