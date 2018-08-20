"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')

import SF_FoodTrucks.views
import SF_FoodTrucks.foodTrucksAPI
