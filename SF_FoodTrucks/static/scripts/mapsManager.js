sfLat = 37.773972
sfLng = -122.431297
var map;
var markers = [];
var currentLocation = { lat: sfLat, lng: sfLng };
var infoWindow;

var foodTruckIconURL = '/static/icons/food-truck-32.png';
var foodCartIconURL = '/static/icons/food-cart-32.png';

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
    infoWindow = new google.maps.InfoWindow({ maxWidth : '250'});
}

function addMarker(location, locationTitle, iconURL, markerInfo, OnClickEventHandler) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: locationTitle,
        icon: iconURL
    });
    marker.info = markerInfo;
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
    $.get('/foodtrucks/GetFoodTrucksNearLocation', { 'locationLat': locationLat, 'locationLng': locationLng, 'maxDistanceInMeters': 750 }, addMarkersToFoodTruckLocations)
}

function addMarkersToFoodTruckLocations(data) {
    var trucks = JSON.parse(data);
    for (var i = 0; i < trucks.length; i++) {
        var truckLocation = { lat: trucks[i].location.coordinates[1], lng: trucks[i].location.coordinates[0] };
        var iconURL = trucks[i].facilitytype == 'Push Cart' ? foodCartIconURL : foodTruckIconURL;
        var truckName = trucks[i].applicant;
        allReviews = $.ajax({
          method: 'GET',
          url: '/reviews/GetTruckReviews?truckID='+trucks[i].objectid,
          async: false
        })
        allReviewsJson = JSON.parse(allReviews.responseText)
        trucks[i].likes = allReviewsJson.likes
        trucks[i].dislikes = allReviewsJson.dislikes

        userReview = $.ajax({
          method: 'GET',
          url: '/reviews/TruckReview?truckID='+trucks[i].objectid,
          async: false
        })

        if (userReview.status != 200)
        {
           trucks[i].userReview = 'Empty'
        }
        else
        {
            userReviewJson = JSON.parse(userReview.responseText)
            trucks[i].userReview = userReviewJson.userReview
        }

        var markerInfo = trucks[i];

        addMarker(truckLocation, truckName, iconURL, markerInfo, handleMarkerClickEvent);
    }
}

function handleMarkerClickEvent() {
    truckID = this.info.objectid;
    windowContent = '<strong>Facility Owner: </strong>' + this.info.applicant + '<br>'
            + '<strong>Facility Type: </strong>' + this.info.facilitytype + '<br>'
            + '<strong>Facility Address: </strong>' + this.info.address + '<br>'
            + '<strong>Food Items: </strong>' + this.info.fooditems + '<br>'
            + '<strong>Working Hours: </strong>' + this.info.dayshours + '<br>'
            + '<strong>Likes: </strong>' + this.info.likes + ' ' +'<strong>Dislikes: </strong>' + this.info.dislikes + '<br>'
            + '<input id = "reviewBtn" type="button" value="Like" onclick="func('+truckID+');"/>';
            infoWindow.setContent(windowContent);
    infoWindow.open(this.getMap(), this);

    if (this.info.userReview == 'Like')
    {
        $('#reviewBtn').attr('value', 'Dislike')
        $('#reviewBtn').attr('style', 'color:red')
    }
    else if (this.info.userReview == 'Dislike')
    {
        $('#reviewBtn').attr('value', 'Like')
        $('#reviewBtn').attr('style', 'color:greed')
    }


}

function func(truckID){
btnVal = $('#reviewBtn').attr('value')
$.post('/reviews/TruckReview?truckID='+truckID, data={'review':btnVal}, toggleReviewButton).fail(function() {alert( "Please log in before submitting your review." );})
}

function toggleReviewButton(){
btnVal = $('#reviewBtn').attr('value')
if (btnVal == 'Like'){
$('#reviewBtn').attr('value', 'Dislike')
$('#reviewBtn').attr('style', 'color:red')
}
else{
$('#reviewBtn').attr('value', 'Like')
$('#reviewBtn').attr('style', 'color:green')
}
}