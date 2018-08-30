from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app, blueprints
)
from SF_FoodTrucks.db import getDB
import json

reviewsBP = Blueprint('reviews', __name__, url_prefix='/reviews')



@reviewsBP.route('/TruckReview', methods=['GET', 'POST'])
def TruckReview():
    """
        Summary:
            Get/Post a review (Like/ Dislike) for a food truck specified by ID.
        Paramters:
        truckID: the ID of the truck to Get/Post review for.
            review: 'Like' or 'Dislike'
        Returns(Incase of Get Request):
            'Like', 'Dislike' or 'Empty'
    """
    userID = session.get('userID')

    if userID is None:
        return 'Please login first.', 401

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

    """
        Summary:
            Get all reviews (number of Likes/ Dislikes) for a food truck specified by ID.
        Paramters:
        truckID: the ID of the truck to Get/Post review for.
        Returns:
            Json object with fields : 'id', 'likes' and 'dislikes'
    """
@reviewsBP.route('/GetTruckReviews', methods=['GET'])
def TruckReviews():
    db = getDB()
    truckID = request.args.get('truckID', type=int)
    if truckID is None:
        return 'Bad request, missing or wrong passed arguments', 400

    response = {'id': truckID, 'likes': 0, 'dislikes': 0}
    truckReviews = db.execute('SELECT * FROM TrucksReviews WHERE id = ?', (truckID,)).fetchone()
    if truckReviews is not None:
        response['likes'] = truckReviews['likes']
        response['dislikes'] = truckReviews['dislikes']

    return jsonify(response), 200


@reviewsBP.route('/GetBestTrucks', methods=['GET'])
def GetBestTrucks():
    """
        Summary:
            Get best food trucks IDs based on difference between likes and dislikes reviews.
        Optional Paramters:
        top: to limit the result.
        Returns:
            Array of json objects of the top best trucks with fields : 'id', 'likes' and 'dislikes'
    """
    db = getDB()
    topLimit = request.args.get('top', type=int)
    if topLimit is None:
        topLimit = 10
    topTrucksRows = db.execute(
        'SELECT * FROM TrucksReviews WHERE (likes-dislikes) > 0 ORDER BY likes-dislikes DESC LIMIT ?',
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
