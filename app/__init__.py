from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'auth.login'

    from .models import User  # Import User model here

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return render_template('home.html')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .game import game as game_blueprint
    app.register_blueprint(game_blueprint)

    return app
