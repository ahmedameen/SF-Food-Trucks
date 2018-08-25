import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from SF_FoodTrucks import create_app, db
from flask import session, url_for


def test_register(client, auth):
    username = 'dummyUsername'
    password = 'dummyPassword'
    error = None
    with client:
        res = auth.register(username, password)
        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')

    assert res.status_code == 302
    assert error is None
    database = db.getDB()
    userRecord = database.execute('SELECT * from users WHERE username = ?',
                                  (username,)).fetchall()
    assert userRecord is not None and len(userRecord) == 1
    dbPassword = userRecord[0]['password']
    assert check_password_hash(dbPassword, password)


@pytest.mark.parametrize(('username', 'password', 'errorMessage'), (
        ('ahmed', 'dummyPassword', 'User ahmed is already registered.'),
        ('', 'dummyPassword', 'Username is required.'),
        ('dummyUsername', '', 'Password is required.'),
))
def test_registerWithErrors(client, auth, username, password, errorMessage):
    error = None
    with client:
        res = auth.register(username, password)
        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')

    assert error is not None and error == errorMessage
    assert res.status_code == 200


def test_login(client, auth):
    username = 'ahmed'
    password = 'ahmedPassword'

    error = None
    userID = None
    with client:
        res = auth.login(username, password)
        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')
        if 'userID' in session:
            userID = session['userID']

    assert res.status_code == 302
    assert error is None
    assert userID is not None


@pytest.mark.parametrize(('username', 'password', 'errorMessage'), (
        ('wrongUsername', 'ahmedPassword', 'Incorrect username.'),
        ('ameen', 'wrongPassword', 'Incorrect password.'),
))
def test_loginWithErrors(client, auth, username, password, errorMessage):
    error = None
    with client:
        res = auth.login(username, password)
        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')
        assert 'userID' not in session

    assert error is not None and error == errorMessage
    assert res.status_code == 200


def test_logout(client, auth):
    username = 'elfiky'
    password = 'elfikyPassword'

    auth.login(username, password)
    error = None
    with client:
        res = auth.logout()
        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')
        assert 'userID' not in session

    assert res.status_code == 302
    assert error is None
