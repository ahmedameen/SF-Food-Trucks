"""
The flask application package.
"""
from flask import Flask
from SF_FoodTrucks import db, auth, views, foodTrucksAPI, trucksReviewsAPI


def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    if testing is False:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_pyfile('testConfig.py')
    app.register_blueprint(auth.authBP)
    app.register_blueprint(views.viewsBP)
    app.register_blueprint(foodTrucksAPI.foodTrucksBP)
    app.register_blueprint(trucksReviewsAPI.reviewsBP)

    db.initApp(app)
    return app
