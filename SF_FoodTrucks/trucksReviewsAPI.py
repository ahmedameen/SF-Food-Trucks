from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app, blueprints
)
from SF_FoodTrucks.db import getDB
import json

reviewsBP = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviewsBP.route('/TruckReview', methods=['GET', 'POST'])
def TruckReview():
    userID = session.get('userID')

    if userID is None:
        return 'Unautharized, please login first.', 401

    db = getDB()
    userRow = db.execute('SELECT * FROM Users WHERE id = ?', (userID,)).fetchone()
    truckID = request.args.get('truckID', type=int)
    if truckID is None:
        return 'Bad request, missing or wrong passed arguments', 400
    userReview = getUserReview(userRow, truckID)
    if request.method == 'GET':
        return jsonify(
            truckID=truckID,
            userReview=userReview), 200
    elif request.method == 'POST':
        if db.execute('SELECT * FROM TrucksReviews WHERE id = ?', (truckID,)).fetchone() is None:
            db.execute('INSERT INTO TrucksReviews (id,likes,dislikes) VALUES (?,?,?)', (truckID, 0, 0))
        userLikes = userRow['trucksLikes'].split(',')
        userDislikes = userRow['trucksDislikes'].split(',')
        newReview = request.form.get('review')
        oldReview = userReview

        if newReview is None:
            return 'Bad request, missing or wrong passed data.', 400

        if newReview == oldReview:
            return 'Review submitted successfully', 200

        if oldReview == 'Dislike':
            userDislikes.remove(str(truckID))
            db.execute('UPDATE TrucksReviews SET dislikes = dislikes - 1 WHERE id = ?', (truckID,))
        elif oldReview == 'Like':
            userLikes.remove(str(truckID))
            db.execute('UPDATE TrucksReviews SET likes = likes - 1 WHERE id = ?', (truckID,))

        if newReview == 'Like':
            userLikes.append(str(truckID))
            db.execute('UPDATE TrucksReviews SET likes = likes + 1 WHERE id = ?', (truckID,))
        elif newReview == 'Dislike':
            userDislikes.append(str(truckID))
            db.execute('UPDATE TrucksReviews SET dislikes = dislikes + 1 WHERE id = ?', (truckID,))

        userLikesStr = ','.join(userLikes)
        userDislikesStr = ','.join(userDislikes)

        db.execute('UPDATE Users SET trucksLikes = ?, trucksDislikes = ? WHERE id = ?',
                   (userLikesStr, userDislikesStr, userID))
        db.commit()
        return 'Review submitted successfully', 200


@reviewsBP.route('/GetBestTrucks', methods=['GET'])
def GetBestTrucks():
    db = getDB()
    topLimit = request.args.get('top', type=int)
    print(topLimit)
    if topLimit is None:
        topLimit = 10
    topTrucksRows = db.execute('SELECT * FROM TrucksReviews ORDER BY likes-dislikes DESC LIMIT ?',
                               (topLimit,)).fetchall()
    topTrucks = [{'id': truckRow['id'], 'likes': truckRow['likes'], 'dislikes': truckRow['dislikes']} for truckRow in
                 topTrucksRows]
    return json.dumps(topTrucks), 200


def getUserReview(userRow, truckID):
    userLikes = userRow['trucksLikes']
    userDislikes = userRow['trucksDislikes']
    userReview = 'Empty'
    trucksLikes = userLikes.split(',')
    trucksDislikes = userDislikes.split(',')
    if str(truckID) in trucksLikes:
        userReview = 'Like'
    elif str(truckID) in trucksDislikes:
        userReview = 'Dislike'
    return userReview