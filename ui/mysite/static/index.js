/* Takes location list from views.py and creates + adds markers to Google map.
Used the following blog for code/inspiration, modified location parameter to 
use our results: https://medium.com/@limichelle21/integrating-google-maps-api-for-multiple-locations-a4329517977a */

var fin_list;
var bounds_list;
var rectangle;

function initMap() {
    var locations = fin_list;
    // Center at top match zip
    var center = {lat: locations[0][1], lng: locations[0][2]};
var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: center
});
var infowindow =  new google.maps.InfoWindow({});
const image = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
const image_top = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png';

for (var count = 0; count < locations.length; count++) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[count][1], locations[count][2]),
        map: map,
        title: locations[count][0],
        icon: count ? image : image_top
    });
google.maps.event.addListener(marker, 'click', (function (marker, count) {
    return function () {
        // Show description
        infowindow.setContent(locations[count][0]);
        infowindow.open(map, marker);

        // draw area
        if (typeof rectangle !== 'undefined') {
            // the rectangle is defined
            rectangle.setMap(null);
            rectangle = undefined;
        } else {
            rectangle = new google.maps.Rectangle({
            strokeColor: "#32A875",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillOpacity: 0,
            map,
            bounds: JSON.parse(bounds_list[count]),
          });
        }
        


   }
    })(marker, count));
}
}       