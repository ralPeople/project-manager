from flask import Flask, render_template, request, redirect, url_for, flash, abort
from login.login import LoginForm
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from createQuiz import *
from db_logic import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.secret_key = '412741253217312'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
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
@app.route('/user/<name>')
def user(name):
    abort(200)
    return '<h1>Hello, %s!</h1>' % name

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Вы уже вошли в акаунт, {current_user.login}")
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        input_login = form.username.data
        input_password = form.password.data

        user = User.query.filter_by(login=input_login).first()
        succes_enter = False

        if(user and user.compare_password(input_password)):
            succes_enter = True

        if(succes_enter):
            flash('Успешный вход пользователя {}'.format(
                form.username.data))
            login_user(user)
            return redirect(url_for('index'))
        flash('Неправильный логин или пароль!', 'error')


    return render_template("login.html", title='Авторизация', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect(url_for('login'))

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = QuizForm()
    if form.validate_on_submit():
        flash('Квиз успешно создан!')
    flash('Пустое имя квиза!', 'error')
    return render_template("quizCreate.html", title='Создание квиза', form=form)

@app.route("/add_question/<int:quiz_id>", methods = ['GET', 'POST'])
@login_required
def add_question(quiz_id):
    form = QuestionForm()

    if request.method == 'GET':
        while len(form.answers) < 4:
            form.answers.append_entry()

        form.correct_index.choices = [(i, f'{i + 1}') for i in range(len(form.answers))]
    '''
     if form.validate_on_submit():
        if form.submit_login.data:
            # Обработка входа
            print("Нажата кнопка Войти")
        elif form.submit_register.data:
            # Обработка регистрации
            print("Нажата кнопка Зарегистрироваться")
    '''
    if form.validate_on_submit():
        question = Question(
            quiz_id = quiz_id,
            question_text = form.question_text.data
        )
        db.session.add(question)
        db.session.flush()
        print(form.answers)

        for i, answer_form in enumerate(form.answers):
            answer = Answer(
                question_id = question.question_id,
                answer_text = answer_form.data['text'],
                is_correct=(i == form.correct_index.data)
            )
            print(answer)
    return render_template('questionCreate.html', form=form, quiz_id=quiz_id)

if __name__ == '__main__':
    app.run(debug=True)



