from app import create_app, db
from app.models import Game, Question
import sys

app = create_app()
app.app_context().push()

def add_questions(game_id):
    questions = [
        ("Who won the FIFA World Cup in 2018?", "Brazil", "Germany", "France", "Argentina", "C"),
        ("Which player has won the most Ballon d'Or awards?", "Cristiano Ronaldo", "Lionel Messi", "Zinedine Zidane", "Johan Cruyff", "B"),
        ("Which club has won the most UEFA Champions League titles?", "Barcelona", "AC Milan", "Liverpool", "Real Madrid", "D"),
        ("Which country hosted the first FIFA World Cup in 1930?", "Brazil", "Italy", "Uruguay", "France", "C"),
        ("Which player scored the 'Hand of God' goal?", "Pelé", "Diego Maradona", "Ronaldinho", "David Beckham", "B"),
        ("Which club is known as 'The Red Devils'?", "Liverpool", "Bayern Munich", "Manchester United", "Arsenal", "C"),
        ("Who is the all-time top scorer for the Premier League?", "Thierry Henry", "Alan Shearer", "Wayne Rooney", "Frank Lampard", "B"),
        ("Which national team is nicknamed 'La Albiceleste'?", "Italy", "Brazil", "Spain", "Argentina", "D"),
        ("In which year did the English Premier League start?", "1990", "1992", "1994", "1996", "B"),
        ("Who holds the record for the fastest goal in World Cup history?", "Cristiano Ronaldo", "Lionel Messi", "Hakan Şükür", "Miroslav Klose", "C"),
    ]

    for question_text, option_a, option_b, option_c, option_d, correct_answer in questions:
        question = Question(
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            game_id=game_id
        )
        db.session.add(question)
    db.session.commit()
    print("Questions added successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_questions.py <game_id>")
    else:
        game_id = int(sys.argv[1])
        add_questions(game_id)
