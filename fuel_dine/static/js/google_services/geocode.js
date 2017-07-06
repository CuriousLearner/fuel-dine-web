function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: {lat: -34.397, lng: 150.644}
  });
  var geocoder = new google.maps.Geocoder();

  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map);
  });
}

function fill_restaurant_form(address, latitude, longitude) {
  // fills the address, longitude and latitude as retrieved from Google
  // Geolocation API to improve user experience.
  document.getElementById('id_address').value = address;
  document.getElementById('id_lat').value = latitude;
  document.getElementById('id_lon').value = longitude;
  // Update Materialize form text fields to consistently move labels up on
  // activating the element.
  $(function() {
    Materialize.updateTextFields();
  });
}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    console.log(results);
    console.log(JSON.stringify(results));
    if (status === 'OK') {
      var address = results[0].formatted_address;
      var latitude = results[0].geometry.location.lat();
      var longitude = results[0].geometry.location.lng();

      // Dynamically fill the add restaurant form based on search location
      fill_restaurant_form(address, latitude, longitude);
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}
