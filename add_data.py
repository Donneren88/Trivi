from app import db
from app.models import User, Question, Game

# Create some users
user1 = User(username='user1', email='user1@example.com', password='password1')
user2 = User(username='user2', email='user2@example.com', password='password2')

# Create a game
game = Game(name='Trivia Game')

# Add questions to the game
question1 = Question(question_text='What is the capital of France?', game=game,
                     option_a='Paris', option_b='London', option_c='Berlin', option_d='Madrid', correct_answer='A')
question2 = Question(question_text='What is 2 + 2?', game=game,
                     option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='B')

# Add to the session
db.session.add(user1)
db.session.add(user2)
db.session.add(game)
db.session.add(question1)
db.session.add(question2)

# Commit the session
db.session.commit()

print("Initial data added successfully!")
