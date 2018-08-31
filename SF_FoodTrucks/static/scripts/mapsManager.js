sfLat = 37.773972
sfLng = -122.431297
var map;
var markers = {};
var markersIDs = []

var infoWindow;

var foodTruckIconURL = '/static/icons/food-truck-32.png';
var foodCartIconURL = '/static/icons/food-cart-32.png';
getTopTrucksIDs()
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

function addMarker(location, locationTitle, iconURL, markerInfo, markerID, OnClickEventHandler) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: locationTitle,
        icon: iconURL
    });
    marker.info = markerInfo;
    marker.addListener('click', OnClickEventHandler);
    markers[markerID] = marker;
    markersIDs.push(markerID);
}

function removeAllMarkers() {
    for (var i = 0; i < markersIDs.length; i++) {
        markers[markersIDs[i]].setMap(null);
    }
    markers = {};
    markersIDs = [];
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
    var currentLocation = this.getPlaces()[0].geometry.location;
    var placeTitle = this.getPlaces()[0].name;
    map.setCenter(currentLocation);
    addMarker(currentLocation, placeTitle);
    getFoodTruckNearLocation(currentLocation.lat, currentLocation.lng);
}


function getFoodTruckNearLocation(locationLat, locationLng) {
    $.get('/foodtrucks/GetFoodTrucksNearLocation', { 'locationLat': locationLat, 'locationLng': locationLng, 'maxDistanceInMeters': 1000 }, addMarkersToFoodTruckLocations)
}

function addMarkersToFoodTruckLocations(data) {
    var trucks = JSON.parse(data);
    for (var i = 0; i < trucks.length; i++) {
      addMarkerToFoodTruckLocation(trucks[i])
    }
}

function addMarkerToFoodTruckLocation(truck){
 var truckLocation = { lat: truck.location.coordinates[1], lng: truck.location.coordinates[0] };
 var iconURL = truck.facilitytype == 'Push Cart' ? foodCartIconURL : foodTruckIconURL;
        var truckName = truck.applicant;
        var markerInfo = truck;

        addMarker(truckLocation, truckName, iconURL, markerInfo, truck.objectid, handleMarkerClickEvent);

        $.get('/reviews/GetTruckReviews', {'truckID':truck.objectid}, function (data){addTruckReviews(data, truck.objectid)})
        $.get('/reviews/TruckReview', {'truckID':truck.objectid},function(data){addTruckUserReview(data, truck.objectid)});
}

function addTruckReviews(data, markerID){
markers[markerID].info.likes = data.likes;
markers[markerID].info.dislikes = data.dislikes;
}

function addTruckUserReview(data, markerID){
markers[markerID].info.userReview = data.userReview;
}

function handleMarkerClickEvent() {
    truckID = this.info.objectid;
    windowContent = '<strong>Facility Owner: </strong>' + this.info.applicant + '<br>'
            + '<strong>Facility Type: </strong>' + this.info.facilitytype + '<br>'
            + '<strong>Facility Address: </strong>' + this.info.address + '<br>'
            + '<strong>Food Items: </strong>' + this.info.fooditems + '<br>'
            + '<strong>Working Hours: </strong>' + this.info.dayshours + '<br>'
            + '<strong>Likes: </strong>' + this.info.likes + ' ' +'<strong>Dislikes: </strong>' + this.info.dislikes + '<br>'
            + '<input id = "likeBtn" type="button" value="Like" onclick="submitLike('+truckID+')";/>'
            + '<input id = "dislikeBtn" type="button" value="Dislike" onclick="submitDislike('+truckID+')";/>';
            infoWindow.setContent(windowContent);
    infoWindow.open(this.getMap(), this);

    if (this.info.userReview == 'Like')
    {
        $('#likeBtn').attr('style', 'color:green')
        $('#dislikeBtn').attr('style', 'color:black')
    }
    else if (this.info.userReview == 'Dislike')
    {
        $('#dislikeBtn').attr('style', 'color:red')
        $('#likeBtn').attr('style', 'color:black')
    }


}

function submitLike(truckID){
$.post('/reviews/TruckReview?truckID='+truckID, data={'review':'Like'}, toggleReviewButtons('Like')).fail(function(xhr, status, error) {alert(xhr.responseText);})
}

function submitDislike(truckID){
$.post('/reviews/TruckReview?truckID='+truckID, data={'review':'Dislike'}, toggleReviewButtons('Dislike')).fail(function(xhr, status, error) {alert(xhr.responseText);})
}

function toggleReviewButtons(review){
    if (review == 'Like'){
        $('#likeBtn').attr('style', 'color:green')
        $('#dislikeBtn').attr('style', 'color:black')
    }
    else {
        $('#dislikeBtn').attr('style', 'color:red')
        $('#likeBtn').attr('style', 'color:black')
    }
}


function getTopTrucksIDs(){
$.get('reviews/GetBestTrucks', {'top':10}, getTopTrucksData)
}

function getTopTrucksData(data){
 trucks = JSON.parse(data);
 topTrucksList = document.getElementById('topTrucksList')
 for (var i = 0; i < trucks.length; i++){
    item = document.createElement('li')
    item.id = 'truck' + trucks[i].id;
    item.setAttribute('data-likes', trucks[i].likes);
    item.setAttribute('data-dislikes', trucks[i].dislikes);
    topTrucksList.appendChild(item)
  }

for(var i = 0; i< trucks.length; i++){
 $.get('/foodtrucks/GetFoodTruck', {'truckID': trucks[i].id}, updateTopTrucksData)
}

}

function updateTopTrucksData(truck){
  var item = $('#truck' + truck.objectid)
  var likes = item.attr('data-likes');
  var dislikes = item.attr('data-dislikes');
  item.html('<a onclick="showOneTruck(this);">'+ truck.applicant + '</a>'+ ' <small>('+likes+' Likes  '+dislikes+ ' Dislikes)</small>' +'<br>'
            + truck.fooditems);
}

function showOneTruck(e){
  var truckID = e.parentNode.id.substring(5)
  $.get('/foodtrucks/GetFoodTruck', {'truckID': parseInt(truckID)},
  function (truck){
  var truckLocation = { lat: truck.location.coordinates[1], lng: truck.location.coordinates[0] };
  map.setCenter(truckLocation);
  map.setZoom(14);
  removeAllMarkers();
  addMarkerToFoodTruckLocation(truck);
  });
}




