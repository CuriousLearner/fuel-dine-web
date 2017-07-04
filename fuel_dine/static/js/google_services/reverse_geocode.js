function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: {lat: 40.731, lng: -73.997}
  });
  var geocoder = new google.maps.Geocoder;
  var infowindow = new google.maps.InfoWindow;

  document.getElementById('submit').addEventListener('click', function() {
      geocodeLatLng(geocoder, map, infowindow);
  });
}

function fill_restaurant_form(address, latitude, longitude) {
  // fills the address, longitude and latitude as retrieved from Google
  // Geolocation API to improve user experience.
  document.getElementById('id_address').value = address;
  document.getElementById('id_lat').value = latitude;
  document.getElementById('id_lon').value = longitude;
}

function geocodeLatLng(geocoder, map, infowindow) {
  var input = document.getElementById('latlng').value;
  var latlngStr = input.split(',', 2);
  var latlng = {lat: parseFloat(latlngStr[0]), lng: parseFloat(latlngStr[1])};
  geocoder.geocode({'location': latlng}, function(results, status) {
    if (status === 'OK') {
      if (results[1]) {
        var address = results[1].formatted_address;
        var latitude = results[1].geometry.location.lat();
        var longitude = results[1].geometry.location.lng();

        // Dynamically fill the add restaurant form based on search location
        fill_restaurant_form(address, latitude, longitude);
        map.setZoom(11);
        var marker = new google.maps.Marker({
          position: latlng,
          map: map
        });
        infowindow.setContent(results[1].formatted_address);
        infowindow.open(map, marker);
      } else {
        window.alert('No results found');
      }
    } else {
      window.alert('Geocoder failed due to: ' + status);
    }
  });
}
