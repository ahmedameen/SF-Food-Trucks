#
import pytest
from flask import json, url_for
from SF_FoodTrucks import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()
    return client

#Test a normal request
def test_normalRequest(client):
    endpoint = '/foodtrucks/GetFoodTrucksNearLocation'
    res = client.get(endpoint + '?locationLat=37.773972&locationLng=-122.431297&maxDistanceInMeters=1000&limit=7')
    assert res.status_code == 200 
    assert b'objectid' in res.data and b'fooditems' in res.data 
    assert len(json.loads(res.data)) <= 7 

#Test a request without an optional paramter (limit)
def test_missingOptionalParamter(client):
    endpoint = '/foodtrucks/GetFoodTrucksNearLocation'
    res = client.get(endpoint + '?locationLat=37.773972&locationLng=-122.431297&maxDistanceInMeters=750')
    assert res.status_code == 200
    assert b'objectid' in res.data and b'fooditems' in res.data 


#Test a request without a mandatory paramter (locationLng)
def test_missingMandatoryParamter(client):
    endpoint = '/foodtrucks/GetFoodTrucksNearLocation'
    res = client.get(endpoint + '?locationLat=37.773972&maxDistanceInMeters=750')
    assert res.status_code == 400

#Test a request with wrong paramter type (maxDistanceInMeters)
def test_wrongParamterType(client):
    endpoint = '/foodtrucks/GetFoodTrucksNearLocation'
    res = client.get(endpoint + '?locationLat=37.773972&locationLng=-122.431297&maxDistanceInMeters=abb')
    assert res.status_code == 400
