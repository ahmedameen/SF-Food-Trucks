sfLat = 37.773972
sfLng = -122.431297
var map;
var markers = [];
var currentLocation = { lat: sfLat, lng: sfLng };

foodTruckIconURL = '/static/icons/food-truck-32.png'
foodCartIconURL = '/static/icons/food-cart-32.png'
function initMap() {
    var mapOptions = {
        center: new google.maps.LatLng(sfLat, sfLng),
        zoom: 11,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    }
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    var searchBoxInput = createSearchBox('locationSearchBox');
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(searchBoxInput);

    var searchBox = new google.maps.places.SearchBox(searchBoxInput);
    searchBox.addListener('places_changed', handleLocationChanged)

    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });
}

function addMarker(location, locationTitle, iconURL, OnClickEventHandler) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: locationTitle,
        icon: iconURL
    });
    marker.addListener('click', OnClickEventHandler);
    markers.push(marker);
}

function removeAllMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

function createSearchBox() {
    searchBox = document.createElement('input');
    searchBox.type = 'text';
    searchBox.id = 'locationSearchBox';
    searchBox.placeholder = 'Search for Location';
    return searchBox;
}


function handleLocationChanged() {
    removeAllMarkers();
    map.setZoom(14);
    currentLocation = this.getPlaces()[0].geometry.location;
    var placeTitle = this.getPlaces()[0].name;
    map.setCenter(currentLocation);
    addMarker(currentLocation, placeTitle);
    getFoodTruckNearLocation(currentLocation.lat, currentLocation.lng);
}


function getFoodTruckNearLocation(locationLat, locationLng) {
    $.get('/GetFoodTrucksNearLocation', { 'locationLat': locationLat, 'locationLng': locationLng, 'maxDistanceInMeters': 750 }, addMarkersToFoodTruckLocations)
}

function addMarkersToFoodTruckLocations(data) {
    var trucks = JSON.parse(data);
    for (var i = 0; i < trucks.length; i++) {
        var truckLocation = { lat: trucks[i].location.coordinates[1], lng: trucks[i].location.coordinates[0] };
        var iconURL = trucks[i].facilitytype == 'Push Cart' ? foodCartIconURL : foodTruckIconURL;
        var truckName = trucks[i].applicant;
        addMarker(truckLocation, truckName, iconURL);
    }
}