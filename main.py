from flask import Flask, render_template, request, redirect, url_for, flash, abort

from flask_login import LoginManager
from flask_login import login_required
from flask_login import logout_user
from quiz.quizForms import *
from db_logic import *
from login.login import auth_login
from login.register import auth_register
from login.logout import auth_logout
from quiz.routes import quiz_route
from flask_login import current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.secret_key = '412741253217312'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Вы должны быть авторизированы для просмотра данной страницы"
login_manager.login_message_category = 'error'


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def base():
    return redirect(url_for('index'))
@app.route('/index')
def index():
    quizes = Quiz.query.filter(Quiz.user_id == current_user.user_id).all()
    for quiz in quizes:

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


app.register_blueprint(auth_login)
app.register_blueprint(auth_register)
app.register_blueprint(auth_logout)
login_manager.login_view = 'auth_login.login'
app.register_blueprint(quiz_route)


if __name__ == '__main__':
    app.run(debug=True)



