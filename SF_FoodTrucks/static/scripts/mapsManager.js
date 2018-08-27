sfLat = 37.773972
sfLng = -122.431297
var map;
var markers = [];
var currentLocation = { lat: sfLat, lng: sfLng };
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
      addMarkerToFoodTruckLocation(trucks[i])
    }
}

function addMarkerToFoodTruckLocation(truck){
 var truckLocation = { lat: truck.location.coordinates[1], lng: truck.location.coordinates[0] };
 var iconURL = truck.facilitytype == 'Push Cart' ? foodCartIconURL : foodTruckIconURL;
        var truckName = truck.applicant;
        allReviews = $.ajax({
          method: 'GET',
          url: '/reviews/GetTruckReviews?truckID='+truck.objectid,
          async: false
        })
        allReviewsJson = JSON.parse(allReviews.responseText)
        truck.likes = allReviewsJson.likes
        truck.dislikes = allReviewsJson.dislikes

        userReview = $.ajax({
          method: 'GET',
          url: '/reviews/TruckReview?truckID='+truck.objectid,
          async: false
        })

        if (userReview.status != 200)
        {
           truck.userReview = 'Empty'
        }
        else
        {
            userReviewJson = JSON.parse(userReview.responseText)
            truck.userReview = userReviewJson.userReview
        }

        var markerInfo = truck;

        addMarker(truckLocation, truckName, iconURL, markerInfo, handleMarkerClickEvent);
}


function handleMarkerClickEvent() {
    truckID = this.info.objectid;
    windowContent = '<strong>Facility Owner: </strong>' + this.info.applicant + '<br>'
            + '<strong>Facility Type: </strong>' + this.info.facilitytype + '<br>'
            + '<strong>Facility Address: </strong>' + this.info.address + '<br>'
            + '<strong>Food Items: </strong>' + this.info.fooditems + '<br>'
            + '<strong>Working Hours: </strong>' + this.info.dayshours + '<br>'
            + '<strong>Likes: </strong>' + this.info.likes + ' ' +'<strong>Dislikes: </strong>' + this.info.dislikes + '<br>'
            + '<input id = "likeBtn" type="button" value="Like" onclick="submitReview('+truckID+', "like");"/> '
            + '<input id = "dislikeBtn" type="button" value="Dislike" onclick="submitReview('+truckID+', "dislike");"/>';
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

function submitReview(truckID, review){
$.post('/reviews/TruckReview?truckID='+truckID, data={'review':review}, toggleReviewButtons(review)).fail(function() {alert( "Please log in before submitting your review." );})
}

function toggleReviewButtons(review){
btnVal = $('#reviewBtn').attr('value')
if (review == 'Like'){
$('#likeBtn').attr('style', 'color:green')
$('#dislikeBtn').attr('style', 'color:black')
}
else{
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




