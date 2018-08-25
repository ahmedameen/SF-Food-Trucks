from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from SF_FoodTrucks.db import getDB

authBP = Blueprint('auth', __name__, url_prefix='/auth')


@authBP.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = getDB()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT ID FROM Users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (username, password, trucksLikes, trucksDislikes) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), '', '')
            )
            db.commit()
            return redirect(url_for('auth.login'), 302)

        flash(error, 'error')

    return render_template('auth/register.html')


@authBP.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = getDB()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE Username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['userID'] = user['ID']
            return redirect(url_for('views.home'), 302)

        flash(error, 'error')

    return render_template('auth/login.html')


@authBP.before_app_request
def loadLoggedInUser():
    userID = session.get('userID')
    if userID is None:
        g.user = None
    else:
        g.user = getDB().execute(
            'SELECT * FROM users WHERE ID = ?', (userID,)
        ).fetchone()


@authBP.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'), 302)
