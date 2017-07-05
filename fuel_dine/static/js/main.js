// Add your javascript code here.

// Get csrf token for AJAX requests
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function displayIncreasedVoteCount() {
  $('#vote-count').text(parseInt($('#vote-count').text()) + 1);
}

function displayDecreasedVoteCount() {
  $('#vote-count').text(parseInt($('#vote-count').text()) - 1);
}
function voteUp(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/restaurant/pk/vote/up".replace('pk', restaurant_id),
    data: {"csrfmiddlewaretoken": csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just upvoted this restaurant!");
    displayIncreasedVoteCount()
  })
  .error(function(msg) {
    alert(msg["responseJSON"]["error"]);
  });
}

function voteDown(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/restaurant/pk/vote/up".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just downvoted this restaurant!");
    displayDecreasedVoteCount()
  })
  .error(function(msg) {
    alert(msg["responseJSON"]["error"]);
  });
}

function thumbsDown(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/restaurant/pk/thumbdown".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just thumbs down this restaurant!");
  })
  .error(function(msg) {
    console.log(JSON.stringify(msg));
    alert(msg["responseJSON"]["error"]);
  });
}

function visited(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/restaurant/pk/visited".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just marked this restaurant as visited!");
  })
  .error(function(msg) {
    console.log(JSON.stringify(msg));
    alert(msg["responseJSON"]["error"]);
  });
}
