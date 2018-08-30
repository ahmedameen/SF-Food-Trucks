from flask import session
from SF_FoodTrucks.db import getDB
import json


# Test if the user sent multi likes and multi dislikes
def test_sendReviews(client, auth):
    username = 'ameen'
    password = 'ameenPassword'
    auth.login(username, password)

    trucksIDs = [30, 100, 45, 55]
    reviews = ['Like', 'Dislike', 'Like', 'Dislike']
    i = 0
    for i in range(len(reviews)):
        error = None
        db = getDB()
        truckStatsBefore = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (trucksIDs[i],)).fetchone()
        with client:
            res = sendReview(client, trucksIDs[i], reviews[i])
            assert res.status_code == 200
            if '_flashes' in session:
                error = dict(session['_flashes']).get('error')

        assert error is None
        truckStatsAfter = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (trucksIDs[i],)).fetchone()
        if reviews[i] == 'Like':
            assertLikeAdded(db, trucksIDs[i], username, truckStatsBefore, truckStatsAfter)
        else:
            assertDislikeAdded(db, trucksIDs[i], username, truckStatsBefore, truckStatsAfter)


# Test if the user at first sent like then sent dislike to the same truck
def test_sendLikeThenDislike(client, auth):
    username = 'ameen'
    password = 'ameenPassword'
    auth.login(username, password)
    truckID = 1
    error = None
    db = getDB()
    truckStatsBefore = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
    with client:
        res1 = sendReview(client, truckID, 'Like')
        assert res1.status_code == 200
        res2 = sendReview(client, truckID, 'Dislike')
        assert res2.status_code == 200

        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')

    assert error is None
    truckStatsAfter = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
    assertDislikeAdded(db, truckID, username, truckStatsBefore, truckStatsAfter)


# Test if the user at first sent dislike then sent like to the same truck
def test_sendDislikeThenLike(client, auth):
    username = 'ameen'
    password = 'ameenPassword'
    auth.login(username, password)
    truckID = 30
    error = None
    db = getDB()
    truckStatsBefore = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
    with client:
        res1 = sendReview(client, truckID, 'Dislike')
        assert res1.status_code == 200
        res2 = sendReview(client, truckID, 'Like')
        assert res2.status_code == 200

        if '_flashes' in session:
            error = dict(session['_flashes']).get('error')

    assert error is None
    truckStatsAfter = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
    assertLikeAdded(db, truckID, username, truckStatsBefore, truckStatsAfter)


# Test if the user at first sent a review (like/dislike) then sent the same review (like/dislike) to the same truck
def test_sendSameReviewTwice(client, auth):
    username = 'ameen'
    password = 'ameenPassword'
    auth.login(username, password)
    truckID = 30
    error = None
    db = getDB()
    review = ['Like', 'Dislike']
    i = 0
    for i in range(2):
        with client:
            res1 = sendReview(client, truckID, review[i])
            assert res1.status_code == 200
            truckStatsBefore = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
            userRowBefore = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
            res2 = sendReview(client, truckID, review[i])
            assert res2.status_code == 200
            truckStatsAfter = db.execute('SELECT * FROM TrucksReviews WHERE ID = ?', (truckID,)).fetchone()
            userRowAfter = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()

            if '_flashes' in session:
                error = dict(session['_flashes']).get('error')

        assert error is None
        assert truckStatsBefore == truckStatsAfter
        assert truckStatsAfter == truckStatsAfter


def test_getBestTrucks(client, auth):
    reviews = [{'username': 'ameen', 'password': 'ameenPassword', 'truckID': 2, 'review': 'Like'},
               {'username': 'elfiky', 'password': 'elfikyPassword', 'truckID': 2, 'review': 'Like'},
               {'username': 'mohamed', 'password': 'mohamedPassword', 'truckID': 4, 'review': 'Like'},
               {'username': 'ahmed', 'password': 'ahmedPassword', 'truckID': 3, 'review': 'Like'},
               {'username': 'ameen', 'password': 'ameenPassword', 'truckID': 3, 'review': 'Like'},
               {'username': 'mohamed', 'password': 'mohamedPassword', 'truckID': 3, 'review': 'Dislike'},
               {'username': 'elfiky', 'password': 'elfikyPassword', 'truckID': 3, 'review': 'Dislike'},
               {'username': 'elfiky', 'password': 'elfikyPassword', 'truckID': 1, 'review': 'Dislike'},
               {'username': 'ahmed', 'password': 'ahmedPassword', 'truckID': 1, 'review': 'Dislike'}]

    trucksOrder = [2, 4]
    i = 0
    for i in range(len(reviews)):
        auth.login(reviews[i]['username'], reviews[i]['password'])
        sendReview(client, reviews[i]['truckID'], reviews[i]['review'])
        auth.logout()

    res = client.get('/reviews/GetBestTrucks')

    assert res.status_code == 200
    retOrder = json.loads(res.data.decode())
    assert len(retOrder) == len(trucksOrder)
    j = 0
    for j in range(len(retOrder)):
        assert retOrder[j]['id'] == trucksOrder[j]


def sendReview(client, truckID, review):
    endPoint = '/reviews/TruckReview?truckID=' + str(truckID)
    return client.post(endPoint, data={'review': review})


def assertLikeAdded(db, truckID, username, truckStatsBefore, truckStatsAfter):
    userRow = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    assert userRow is not None
    assert str(truckID) in userRow['trucksLikes']
    assert str(truckID) not in userRow['trucksDislikes']

    assert truckStatsAfter is not None
    if truckStatsBefore is None:
        assert truckStatsAfter['dislikes'] == 0 and truckStatsAfter['likes'] == 1
    else:
        assert truckStatsAfter['likes'] == truckStatsBefore['likes'] + 1
        assert truckStatsAfter['dislikes'] == truckStatsBefore['dislikes']


def assertDislikeAdded(db, truckID, username, truckStatsBefore, truckStatsAfter):
    userRow = db.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    assert userRow is not None
    assert str(truckID) in userRow['trucksDislikes']
    assert str(truckID) not in userRow['trucksLikes']

    assert truckStatsAfter is not None
    if truckStatsBefore is None:
        assert truckStatsAfter['dislikes'] == 1 and truckStatsAfter['likes'] == 0
    else:
        assert truckStatsAfter['dislikes'] == truckStatsBefore['dislikes'] + 1
        assert truckStatsAfter['likes'] == truckStatsBefore['likes']
