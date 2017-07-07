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
  $('.vote-count').text(parseInt($('.vote-count').text()) + 1);
}

function displayDecreasedVoteCount() {
  $('.vote-count').text(parseInt($('.vote-count').text()) - 1);
}

function tryDisplayErrorAlert(msg) {
  try {
    alert(msg["responseJSON"]["error"]);
  }
  catch(err) {
    console.log(err);
    alert("Oops! Something went wrong! Please try again later");
  }
}

function normalizeDate(d) {
  return d.toString();
}

function voteUp(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/api/restaurant/pk/vote/up/".replace('pk', restaurant_id),
    data: {"csrfmiddlewaretoken": csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just upvoted this restaurant!");
    displayIncreasedVoteCount()
  })
  .error(function(msg) {
    tryDisplayErrorAlert(msg);
  });
}

function voteDown(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/api/restaurant/pk/vote/down/".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just downvoted this restaurant!");
    displayDecreasedVoteCount()
  })
  .error(function(msg) {
    tryDisplayErrorAlert(msg);
  });
}

function thumbsDown(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/api/restaurant/pk/thumbdown/".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just thumbs down this restaurant!");
  })
  .error(function(msg) {
    tryDisplayErrorAlert(msg);
  });
}

function visited(restaurant_id) {
  $.ajax({
    method: "POST",
    url: "/api/restaurant/pk/visited/".replace('pk', restaurant_id),
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    alert("You just marked this restaurant as visited!");
  })
  .error(function(msg) {
    tryDisplayErrorAlert(msg);
  });
}

function populateRestaurantList() {
    $.ajax({
    method: "GET",
    url: "api/restaurant/",
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    var results = msg["results"];

    // Clear message of no restaurants to display from the DOM
    $('#restaurant-list').text("");
    for (var i=0; i < results.length; i++) {
      var html_text = `
        <div class="row">
          <div class="col s12 m12">
            <div class="card blue-grey darken-1">
              <div class="card-content white-text">
                <span class="card-title">restaurant_name</span>
                  <p>Votes:&nbsp; restaurant_vote_score</p>
                  <p>Contact:&nbsp; restaurant_contact</p>
                  <p>Website:&nbsp; restaurant_website</p>
                  <p>Description:&nbsp; restaurant_description</p>
              </div>
              <div class="card-action">
                <a href="restaurant_detail_url">See details for this restaurant</a>
              </div>
            </div>
          </div>
        </div>`;

      var variable_mapping = {
        "restaurant_name": results[i]["name"],
        "restaurant_vote_score": results[i]["vote_score"] || 0,
        "restaurant_contact": results[i]["contact"] || '',
        "restaurant_website": results[i]["website"] || '',
        "restaurant_description": results[i]["description"] || '',
        "restaurant_detail_url": "/restaurant/" + results[i]["id"]
      };
      var re = new RegExp(Object.keys(variable_mapping).join("|"),"gi");
      actual_html = html_text.replace(re, function(matched){
        return variable_mapping[matched];
      });
      $('#restaurant-list').append(actual_html);
    }
  })
  .error(function(msg) {
    alert("Something went wrong! Please try again later");
    console.log(msg)
  });
}

var my_email = null;

function get_my_email() {
  $.ajax({
    method: "GET",
    url: "/api/me/"
  })
  .done(function(msg) {
    console.log("Got current_user mail as " + msg["email"]);
    my_email = msg["email"];
  })
  .error(function(msg) {
    console.log("Some error occurred in getting current user mail");
    return "admin@localhost.com";
  });
}

function populateRestaurantDetail(restaurant_id) {
  $.ajax({
    method: "GET",
    url: "/api/restaurant/" + restaurant_id,
    data: {csrfmiddlewaretoken: csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    var result = msg;
    // For knowing email of current user to match it for adding special
    // symbol to any review posted by me.
    var html_text = `
          <b>Name</b>:&nbsp; restaurant_name<br>
          <b>Votes</b>:
          <span class="vote-count">&nbsp;restaurant_vote_score</span>

          <div class="right">
            <a class="waves-effect waves-light btn" href="#"
               onclick="voteUp(id);">
              <i class="material-icons arrow_upward">arrow_upward</i>
            </a>
            <a class="waves-effect waves-light btn" href="#"
               onclick="voteDown(id);">
              <i class="material-icons arrow_downward">arrow_downward</i>
            </a>
            <a class="waves-effect waves-light btn" href="#"
               onclick="thumbsDown(id);">
              <i class="material-icons thumb_down">thumb_down</i>
            </a>
            <a class="waves-effect waves-light btn" href="#"
               onclick="visited(id);">
              <i class="material-icons visited">room</i>
            </a>
          </div>
          <br>
          <b>Contact</b>:&nbsp;restaurant_contact<br>
          <b>Website</b>:&nbsp;restaurant_website<br>
          <b>Description</b>:&nbsp;restaurant_description<br>
        </p>
        <p>Write a <a href="post_new_review_url"><b>&nbsp;new review&nbsp;</b></a> for this restaurant now!</p>
        <hr>
    `;
    if(result["reviews"]) {
      for(var i in result["reviews"]) {
        //console.log(i['text']);
        //console.log("result review");
        //console.log(result["reviews"]);

        var current_review_user = result["reviews"][i]["user"];

        html_text += `        <b>Reviews</b>:
        <div class="review">
        `;
        if (my_email == current_review_user) {

          // Inserts special symbol in the DOM for my own reviews.
          html_text +=   `<b>
              <i class="material-icons">face</i>
          </b>
          `;
        }

        html_text += `<small><b>`;

        html_text += current_review_user;

        html_text += `</b>&nbsp;added review on&nbsp;`;

        html_text += normalizeDate(result["reviews"][i]["posted_at"]);
        html_text += `</small>
        <br>`;

        html_text += result["reviews"][i]["text"];

        html_text += `<br>
        <small><a href="`;

        html_text += "/review/" + result["reviews"][i]["id"] + "/comment/";

        html_text += `"><b>Comment on this review</b></a></small>
      </div>
        `;

        // Check for comments for this review and render them.

        if(result["reviews"][i]["comments"]) {

          for(var j in result["reviews"][i]["comments"]) {
            var comment = result["reviews"][i]["comments"];

            html_text += `<div class="comments">
                <small><b>`;
            html_text += comment[j]["user"];

            html_text += `</b>&nbsp;commented on&nbsp;`;

            html_text += normalizeDate(comment[j]["posted_at"])

            html_text += `</small><br>
                <div class="comment-text">`;

            html_text += comment[j]["text"];

            html_text += `</div>
              </div>
              <hr>
              `;
          }
        }
      }
    }

    var variable_mapping = {
      "restaurant_name": result["name"],
      "restaurant_vote_score": result["vote_score"] || 0,
      "restaurant_contact": result["contact"] || '',
      "restaurant_website": result["website"] || '',
      "restaurant_description": result["description"] || '',
      "id": result["id"],
      "post_new_review_url": "/restaurant/" + result["id"] + "/review/"
    };
    var re = new RegExp(Object.keys(variable_mapping).join("|"),"gi");
    actual_html = html_text.replace(re, function(matched){
      return variable_mapping[matched];
    });
    $('#restaurant-detail-view').append(actual_html);
  })
  .error(function(msg) {
    alert("Something went wrong! Please try again later");
    console.log(msg);
  });
}

$("#add-restaurant").submit(function(e) {

    var url = "/api/restaurant/";
    var data = {
      "name": $('#id_name').val(),
      "lat": $('#id_lat').val(),
      "lon": $('#id_lon').val(),
      "description": $('#id_description').val(),
      "address": $('#id_address').val(),
      "website": $('#id_website').val(),
      "contact": $('#id_contact').val(),
      "csrfmiddlewaretoken": csrftoken
    };
    console.log(data);
    $.ajax({
       type: "POST",
       url: url,
       data: data,
       success: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Restaurant added successfully.");
       },
       error: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Something went wrong! Please try again later.");
       }
    });

  e.preventDefault();
  return false;
});

$("#add-review").submit(function(e) {

    var url = "/api/restaurant/" + $('#restaurant_id').val() + "/review/";
    var data = {
      "text": $('#id_review_text').val(),
      "restaurant": $('#restaurant_id').val(),
      "user": $('#user_id').val(),
      "csrfmiddlewaretoken": csrftoken
    };
    $.ajax({
       type: "POST",
       url: url,
       data: data,
       success: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Review added successfully.");
       },
       error: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Something went wrong! Please try again later.");
       }
    });

  e.preventDefault();
  return false;
});

$("#add-comment").submit(function(e) {
    var url = "/api/review/" +  $('#review_id').val()  + "/comment/";
    var data = {
      "text": $('#id_comment_text').val(),
      "review": $('#review_id').val(),
      "user": $('#user_id').val(),
      "csrfmiddlewaretoken": csrftoken
    };
    $.ajax({
       type: "POST",
       url: url,
       data: data,
       success: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Comment added successfully.");
       },
       error: function(data) {
         console.log(JSON.stringify(data));
         $('#submit-result').text("Something went wrong! Please try again later.");
       }
    });
  e.preventDefault();
  return false;
});


$(document).ready(function() {
  // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
  $('.modal').modal();
});


$('#vote-count-res').click(function() {
  $.ajax({
    method: "GET",
    url: "/api/results/",
    data: {"csrfmiddlewaretoken": csrftoken}
  })
  .done(function(msg) {
    console.log(msg);
    var result = msg["result"];
    var html_res_text = "";
    for (var i in result) {
      html_res_text += "<p><b>Name</b>: " + result[i]["name"] + "</p>";
      html_res_text += "<p><b>Contact</b>: " + result[i]["contact"] + "</p>";
      html_res_text += "<p><b>Address</b>: " + result[i]["address"] + "</p>";
      html_res_text += "<p><b>Votes</b>: " + result[i]["vote_score"] + "</p><hr>";
    }
    // Empty previous result value first and then udpate DOM with new result.
    $('#modal-content-res').text("");
    $('#modal-content-res').append(html_res_text);
  })
  .error(function(msg) {
    console.log(msg);
    $('#modal-content-res').text("oops! Couldn't retrieve results at this time!");
  });
});


// This API would take much time, so dropping this extra feature for now.

//$('#reset-vote-count').click(function() {
//  $.ajax({
//    method: "DELETE",
//    url: "api/votes/reset/",
//    data: {"csrfmiddlewaretoken": csrftoken}
//  })
//  .done(function(msg) {
//    console.log(msg);
//    $('#reset-count-res').text("Count reset successfully!");
//
//  })
//  .error(function(msg) {
//    console.log(msg);
//    $('#reset-count-res').text("Oops, something went wrong!");
//  });
//});
