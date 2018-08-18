sfLat = 37.773972
sfLng = -122.431297
var map;
var markers = [];
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
    searchBox.addListener('places_changed', function () { map.setZoom(13);map.setCenter(searchBox.getPlaces()[0].geometry.location); addMarker(searchBox.getPlaces()[0].geometry.location); })

    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });
}

function addMarker(location, locationTitle, OnClickEventHandler) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: locationTitle
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

