"""
The flask application package.
"""
from flask import Flask
from SF_FoodTrucks import db

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')
db.initApp(app)

from SF_FoodTrucks import auth

app.register_blueprint(auth.authBP)

import SF_FoodTrucks.views
import SF_FoodTrucks.foodTrucksAPI
