var map;

function init() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(initialLocation);
        });
    }
    else {
        var initialLocation = new google.maps.LatLng(53.65914, 0.072050);
    }

    var mapOptions = {
        zoom: 10,
        center: initialLocation,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
}

google.maps.event.addDomListener( window, 'load', init );


function draw_route(routeCoords, map) {
    console.log("drawing route on map: " + map.getCenter());
    var route = new google.maps.Polyline({
        path: routeCoords,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 1,
        map: map
    });
    route.setMap(map);
    var pos = new google.maps.LatLng(routeCoords[0].lat(), routeCoords[0].lng());
    map.panTo(pos);
    map.setZoom(14);
}


var arrCoords2 = [
    new google.maps.LatLng(53.358647,-1.485686),
    new google.maps.LatLng(53.358719,-1.485568),
    new google.maps.LatLng(53.372861, -1.73216)
];

$(document).ready(function() {
    $('.route_name').bind('click', function() {
        var target = event.target || event.srcElement
        $.getJSON($SCRIPT_ROOT + '/_get_coords', {
            // Send this to the server
            name: target.innerHTML
        }, function(data) {
            // Do this to whatever the server sends back  
            var arrCoords = [];
            var x = new google.maps.LatLng(data.result[3][0], data.result[3][1]);
            
            for (i = 0; i < data.result.length; i++) {
                // console.log("add");
                if ( i % 2 == 0) {
                    arrCoords.push(new google.maps.LatLng(data.result[i][0], data.result[i][1]));
                }     
            }
            console.log(arrCoords[15].lng() + ", " + arrCoords[15].lat());
            draw_route(arrCoords, map);
        });
        
    });
});





