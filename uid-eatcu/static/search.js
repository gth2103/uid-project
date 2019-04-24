//@TODO: limit search  space  to type:  restaurants,  food


var columbia;
var map;
var radius;
var request;
var keyword;

var input;
var searchBox;
var markers;

var places;

var bounds;
var icon;

var request;
var infowindow;
var infocontents;

var service;
var marker;

var entry;
var restaurant_exists;
var appointment_exists;


var green = "green";
var red = "red";
var yellow = "yellow";

function clearMarkers() {

    // Clear out the old markers.

    markers.forEach(function(marker) {
        marker.setMap(null);
    });

    markers = [];
}

var search = function(newItem, appointment){
    var item_to_add = newItem
    $.ajax({
        type: "POST",
        url: "search?appointment=" + appointment,                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(item_to_add),
        success: function(result){
            console.log(result);
            location.reload();
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function initMap() {
    columbia = new google.maps.LatLng(40.8070, -73.9630);
    map = new google.maps.Map(document.getElementById('map'), {
        center: columbia,
        zoom: 16,
        mapTypeId: 'roadmap'
    });

    // Create the search box and link it to the UI element.

    input = document.getElementById('search-discover-input');
    searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.

    map.addListener('bounds_changed', function() {
           searchBox.setBounds(map.getBounds());
    });

    markers = [];

    searchBox.addListener('places_changed', function() {
        places = searchBox.getPlaces();

        if (places.length == 0) {
          return;
        }

       // For each place, get the icon, name and location.

       places.forEach(function(place) {

          if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
          }

          restaurant_exists = false;

          restaurants.forEach(function(restaurant) {

              if (restaurant.id == place.id) {
                 restaurant_exists = true;
              }
          });

          if (!restaurant_exists) { 
              entry = {
              title: place.name,
              id: place.id,
              address: place.formatted_address,
              icon: place.icon,
              position: place.geometry.location
              } 
              search(entry, false);
          }

          setIcons(); 

      });
      location.reload();
  });
}

function setIcon(restaurant, color) {

          icon = {
              url: "http://maps.google.com/mapfiles/ms/icons/" + color + "-dot.png",
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
          };

          // Create a marker for a place.
 
          markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: restaurant.name,
              position: restaurant.position
          }));
}

function setIcons() { 
    restaurants.forEach(function(restaurant) {

        //@TODO: conditional statemenet to  set icon red/yellow/green based on appointment status

        setIcon(restaurant, red);
 
        markers.forEach(function(marker) {

            infowindow = new google.maps.InfoWindow();

            //@TODO: conditional, if in appointments infocontents = item, else form



            google.maps.event.addListener(marker, 'click', function() {

                appointment_exists = false;

                appointments.forEach(function(appointment) {

                    if (appointment.id == restaurant.id) {
        
                    setIcon(restaurant, green);

                    infocontents = '<br><div><p><strong><big><b>' + appointment.title + '</b></big></strong></p><br><p><span class="info">Date: </span>' + appointment.date + '</p><p><span class="info">Start time: </span>' + appointment.starttime + '</p><br><p><span class="info">End time: </span>' + appointment.endtime + '</p><br><p><span class="info">Notes: </span><br><span class="notes">' + appointment.notes + '</span></p></div'
                        appointment_exists = true;
                    }
                });

                if(!appointment_exists) {

                    setIcon(restaurant, red);

                    infocontents = '<div class="row m-2 ml-4 mt-4"><div class="col-10 ml-5"><form id="add_item_form"><div class="form-group"><input id="id" class="form-control" type="hidden" value="' + restaurant.id + '"></div><div class="form-group"><label for="title">Place:</label><input id="title" class="form-control" type="text" aria-describedby="titleHelp" placeholder="' + restaurant.title + '" minlength="2" readonly></div><div class="form-group"><label for="date">Date:</label><input id="date" class="form-control" type="text" aria-describedby="dateHelp" placeholder="mm/dd/yyyy" required><small id="dateHelp" class="form-text text-muted">Please enter the date in the specified format.</small></div><div class="form-group"><label for="starttime">Start time:</label><input id="starttime" class="form-control time" type="time" aria-describedby="starttimeHelp" placeholder="h:mm p" required><small id="starttimeHelp" class="form-text text-muted">Please enter the start time in the specified format.</small></div><div class="form-group"><label for="endtime">End time:</label><input id="endtime" class="form-control time" type="time" aria-describedby="endtimeHelp" placeholder="h:mm p" required><small id="endtimeHelp" class="form-text text-muted">Please enter the end time in the specified format.</small></div><div class="form-group"><label for="textareaNotes">Notes:</label><textarea class="form-control" id="textareaSummary" rows="3"></textarea></div><input id="submit" type="submit" class="btn btn-primary mb-5" value="Submit"></form></div></div>'
                }
 
                infowindow.setContent(infocontents);
                
                google.maps.event.addListener(infowindow, 'domready', function() {

                // Bind the click event on your button here

                    $('#submit').on('click', function(e){

                        e.preventDefault();

                        setIcon(restaurant, yellow);

                        var id = $('input#id').val()
                        var title = $('input#title').val()
                        var date = $('input#date').val()
                        var starttime = $('input#starttime').val()
                        var endtime = $('input#endtime').val()
                        var notes = $.trim($('textarea#textareaNoes').val()).replace(/\"/g, "\\\"")

                        var newItem = jQuery.parseJSON( '{ "id": "' + id + '", "title": "' + title + '", "date": "' + date + '", "starttime": "' + starttime + '",  "endtime": "' + endtime + '", "notes": "' + notes + '" }')

                        search(newItem, true)
                    });
                });

                infowindow.open(map, this);
                
            });
        });
    });
}

var appointments = appointments;
console.log(appointments)

$(document).ready(function(){


    $('#search-discover-input').attr("placeholder","Enter search...");
    setIcons();

    $( "#date" ).datepicker();
    $(".time").timepicker({
        timeFormat: 'h:mm p',
        interval: 30,
        minTime: '6:00am',
        maxTime: '11:30pm',
        defaultTime: '12:00pm',
        startTime: '6:00am',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});

