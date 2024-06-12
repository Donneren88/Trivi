from app import db
from sqlalchemy.schema import UniqueConstraint, ForeignKeyConstraint

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('username', name='uq_user_username'),
        UniqueConstraint('email', name='uq_user_email'),
    )

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    questions = db.relationship('Question', backref='game', lazy=True)

    __table_args__ = (
        UniqueConstraint('name', name='uq_game_name'),
    )

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['game_id'], ['game.id'], name='fk_question_game_id'),
    )
