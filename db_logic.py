from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def compare_password(self, password):
        return check_password_hash(self.password, password)
    def get_id(self):
        return str(self.user_id)

class Quiz(db.Model):
    __tablename__ = 'quiz'

    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # связь с создателем
    title = db.Column(db.String(150), nullable=False)

    # Связь с пользователем (чтобы удобно получать автора квиза)
    creator = db.relationship('User', backref=db.backref('quiz_list', lazy=True))

class QuizResult(db.Model):
    __tablename__ = 'quizres'

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer)
    percent = db.Column(Numeric(5,2))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)

    quiz = db.relationship('Quiz', backref=db.backref('question_list', lazy=True))

class Answer(db.Model):
    __tablename__ = 'answer'

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer_text = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    question = db.relationship('Question', backref=db.backref('answer_list',lazy=True))



