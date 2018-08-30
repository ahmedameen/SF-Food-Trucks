import pytest
from SF_FoodTrucks import create_app, db
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app(testing=True)
    appContext = app.app_context()
    appContext.push()
    initDBForTesting()
    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


@pytest.fixture
def auth(client):
    return AuthManager(client)


def initDBForTesting():
    db.initDB()
    database = db.getDB()
    usernames = ['ahmed', 'ameen', 'mohamed', 'elfiky']
    passwords = ['ahmedPassword', 'ameenPassword', 'mohamedPassword', 'elfikyPassword']
    i = 0
    for i in range(len(usernames)):
        database.execute('INSERT INTO Users (username,password, trucksLikes, trucksDislikes) VALUES (?,?,?,?)',
                         (usernames[i], generate_password_hash(passwords[i]), '', ''))
    database.commit()
    return


class AuthManager(object):
    def __init__(self, _client):
        self.client = _client

    def register(self, username, password):
        endpoint = '/auth/register'
        data = {'username': username, 'password': password}
        return self.client.post(endpoint, data=data)

    def login(self, username, password):
        endpoint = '/auth/login'
        data = {'username': username, 'password': password}
        return self.client.post(endpoint, data=data)

    def logout(self):
        endpoint = '/auth/logout'
        return self.client.get(endpoint)
