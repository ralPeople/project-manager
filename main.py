from flask import Flask, render_template, redirect, url_for
import os
import secrets

from flask_login import LoginManager


from graph.classes import *
from graph.build.graphInit import build_graph
from graph.draw.draw import draw_graph

from index.index import bp_index
from project_network.createModel import bp_create_model
from project_gantt.createGantt import bp_create_gantt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SECRET_KEY'] = secrets.token_hex(64)


app.register_blueprint(bp_index)
app.register_blueprint(bp_create_model)
app.register_blueprint(bp_create_gantt)

@app.route('/')
def base():
    return redirect(url_for('bp_index.index'))

if __name__ == '__main__':
    if os.environ.get("RENDER") is None:  # Проверяем, что это не Render
        app.run(debug=True)



