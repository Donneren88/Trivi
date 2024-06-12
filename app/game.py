from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from .models import User
from . import db
import random

game = Blueprint('game', __name__)

PREDEFINED_QUESTIONS = [
    {
        "question_text": "Who won the FIFA World Cup in 2018?",
        "option_a": "Brazil",
        "option_b": "Germany",
        "option_c": "France",
        "option_d": "Argentina",
        "correct_answer": "C"
    },
    {
        "question_text": "Which player has won the most Ballon d'Or awards?",
        "option_a": "Cristiano Ronaldo",
        "option_b": "Lionel Messi",
        "option_c": "Zinedine Zidane",
        "option_d": "Johan Cruyff",
        "correct_answer": "B"
    },
    {
        "question_text": "Which club has won the most UEFA Champions League titles?",
        "option_a": "Barcelona",
        "option_b": "AC Milan",
        "option_c": "Liverpool",
        "option_d": "Real Madrid",
        "correct_answer": "D"
    },
    {
        "question_text": "Which country hosted the first FIFA World Cup in 1930?",
        "option_a": "Brazil",
        "option_b": "Italy",
        "option_c": "Uruguay",
        "option_d": "France",
        "correct_answer": "C"
    },
    {
        "question_text": "Which player scored the 'Hand of God' goal?",
        "option_a": "Pelé",
        "option_b": "Diego Maradona",
        "option_c": "Ronaldinho",
        "option_d": "David Beckham",
        "correct_answer": "B"
    },
    {
        "question_text": "Which club is known as 'The Red Devils'?",
        "option_a": "Liverpool",
        "option_b": "Bayern Munich",
        "option_c": "Manchester United",
        "option_d": "Arsenal",
        "correct_answer": "C"
    },
    {
        "question_text": "Who is the all-time top scorer for the Premier League?",
        "option_a": "Thierry Henry",
        "option_b": "Alan Shearer",
        "option_c": "Wayne Rooney",
        "option_d": "Frank Lampard",
        "correct_answer": "B"
    },
    {
        "question_text": "Which national team is nicknamed 'La Albiceleste'?",
        "option_a": "Italy",
        "option_b": "Brazil",
        "option_c": "Spain",
        "option_d": "Argentina",
        "correct_answer": "D"
    },
    {
        "question_text": "In which year did the English Premier League start?",
        "option_a": "1990",
        "option_b": "1992",
        "option_c": "1994",
        "option_d": "1996",
        "correct_answer": "B"
    },
    {
        "question_text": "Who holds the record for the fastest goal in World Cup history?",
        "option_a": "Cristiano Ronaldo",
        "option_b": "Lionel Messi",
        "option_c": "Hakan Şükür",
        "option_d": "Miroslav Klose",
        "correct_answer": "C"
    }
]

@game.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@game.route('/play')
@login_required
def play_game():
    session['current_question'] = 0
    session['score'] = 0
    session['questions_order'] = random.sample(range(len(PREDEFINED_QUESTIONS)), len(PREDEFINED_QUESTIONS))
    return redirect(url_for('game.next_question'))

@game.route('/play/question')
@login_required
def next_question():
    questions = PREDEFINED_QUESTIONS
    current_question_index = session.get('current_question', 0)
    questions_order = session.get('questions_order', [])

    if current_question_index >= len(questions):
        current_user.score += session['score']
        db.session.commit()
        return redirect(url_for('game.show_score'))

    question = questions[questions_order[current_question_index]]
    return render_template('play_game.html', question=question, question_number=current_question_index + 1)

@game.route('/play/answer', methods=['POST'])
@login_required
def answer_question():
    questions = PREDEFINED_QUESTIONS
    current_question_index = session.get('current_question', 0)
    questions_order = session.get('questions_order', [])
    selected_answer = request.form.get('answer')
    correct_answer = questions[questions_order[current_question_index]]['correct_answer']

    if selected_answer == correct_answer:
        session['score'] += 1
        flash('Correct!', 'success')
    else:
        flash('Wrong!', 'danger')

    session['current_question'] = current_question_index + 1
    return redirect(url_for('game.next_question'))

@game.route('/play/score')
@login_required
def show_score():
    score = session.get('score', 0)
    return render_template('score.html', score=score)

@game.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)
