from SF_FoodTrucks import app
import requests
from flask import request


@app.route('/GetFoodTrucksNearLocation', methods=['GET'])
def GetFoodTrucksNearLocation():
    apiEndPoint = 'https://data.sfgov.org/resource/6a9r-agq8.json'
    appToken = app.config['SF_APP_TOKEN']
    locationLat = request.args.get('locationLat', type=float)
    locationLng = request.args.get('locationLng', type=float)
    maxDistanceInMeters = request.args.get('maxDistanceInMeters', type=float)
    if locationLat is None or locationLng is None or maxDistanceInMeters is None:
        return 'Bad request, missing or wrong passed arguments. Please review the API documentation for the correct format.', 400
    limit = request.args.get('limit', type=int)
    query = '?$where=within_circle(Location, '+str(locationLat)+', '+str(locationLng)+', '+str(maxDistanceInMeters)+')'
    params = {'$$app_token' : appToken}
    if limit is not None:
        params['$limit'] = limit
    req = requests.get(apiEndPoint+query, params)
    return req.content, 200