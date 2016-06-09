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
        minZoom: 2,
        center: initialLocation,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
}

google.maps.event.addDomListener( window, 'load', init );
google.maps.event.addDomListener( window, 'load', loadRoutes );

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

}

$(document).ready(function() {
    $('.route_name').bind('click', function() {
        var target = event.target || event.srcElement
        $.getJSON($SCRIPT_ROOT + '/_get_bounds', {
            // Send this to the server
            name: target.innerHTML,
            id: target.id
        }, function(data) {
            // Do this to whatever the server sends back  
            var NE = new google.maps.LatLng(data.result["NElat"], data.result["NElng"]);
            var SW = new google.maps.LatLng(data.result["SWlat"], data.result["SWlng"]);
            var bounds =  new google.maps.LatLngBounds(SW, NE);
            map.fitBounds(bounds);
        });
    });
});


$(document).ready(function() {
    $('.fit_routes').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/_user_bounds', {
        }, function(data) { 
            var NE = new google.maps.LatLng(data.result["NElat"], data.result["NElng"]);
            var SW = new google.maps.LatLng(data.result["SWlat"], data.result["SWlng"]);
            console.log("fit bounds");
            console.log("NE: (" + data.result["NElat"] +", " + data.result["NElng"] + ")");
            console.log("SW: (" + data.result["SWlat"] +", " + data.result["SWlng"] + ")");
            var bounds =  new google.maps.LatLngBounds(NE, SW);
            console.log(bounds);
            map.fitBounds(bounds);
        });
    });
})


function loadRoutes() {
    $.getJSON($SCRIPT_ROOT + '/_get_routes', {
    },
    function(data) {
        console.log(data.result);
        for (route in data.result) {
            // console.log(data.result[route]);
            var Coords = [];
            for (i = 0; i < data.result[route].length-3; i = i + 3) {
                console.log('a');
                Coords.push(new google.maps.LatLng(data.result[route][i][1], data.result[route][i][0]));
            }
            draw_route(Coords, map);
        }
    })
};


Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};


