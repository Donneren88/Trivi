from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('game.dashboard'))
        else:
            flash('Login failed. Check your email and password.')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.')
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('game.dashboard'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
