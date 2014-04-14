<!DOCTYPE HTML>
<head>
  <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" />
  <link rel="stylesheet" href="style.css" />
 <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
  <script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>
  <script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.2/jquery.ui.touch-punch.min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.2/jquery.ui.touch-punch.min.js"></script>
  <script>
    OSM_URL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    OSM_ATTRIB = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors';
  </script>
</head>
<body>
  <div id="map"></div>
  <script>
    // initialize the map on the "map" div with a given center and zoom
    var map = L.map('map', {
      center: [40, -100],
      zoom: 4
    });
    // Adding the actual map tiles
    var r = 3;
    var o = 1.0;
    L.tileLayer(OSM_URL, {attribution: OSM_ATTRIB}).addTo(map);
    <?php echo file_get_contents("../clustering/points.txt") ?>
    <?php echo file_get_contents("../clustering/hulls.txt") ?>

//Start Time Slider code
myControl = L.control({position: 'topright'});
myControl.onAdd = function(map) {
            this._div = L.DomUtil.create('div', 'GraphControl');
            this._div.innerHTML = '<span height="60" width="60" style="float:right;padding-right:10px;padding-top:10px;z-index:2;color:grey;">&nbsp&nbsp<label><b>Prediction for year 2014 Q</b></label>&nbsp&nbsp:&nbsp&nbsp<span id="pred" style="font-weight:bold">0</span><br/><image id="image1" src="http://atr.eng.utah.edu/~senguttu/drug/viz/graph.jpg" height="300" width="400"/></span>';
            return this._div;
}
myControl.addTo(map);


myControl = L.control({position: 'bottomright'});
myControl.onAdd = function(map) {
            this._div = L.DomUtil.create('div', 'myControl');
            this._div.innerHTML = '<label>Enter Start Year (for prediction): </label><input type="text" value="1951" id="yearsearch" />'; 
            return this._div;
}
myControl.addTo(map);

//Functions to either disable (onmouseover) or enable (onmouseout) the map's dragging
function controlEnter(e) {
    map.dragging.disable();
}
function controlLeave() {
    map.dragging.enable();
N}

//Quick application to all input tags
///*
var inputTags = document.getElementsByTagName("input")
for (var i = 0; i < inputTags.length; i++) {
    inputTags[i].onmouseover = controlEnter;
    inputTags[i].onmouseout = controlLeave;
}
//*/

// --- OR ---

//Quick application of event handlers to overall control
/*
document.getElementsByClassName("myControl")[0].onmouseover = controlEnter;
document.getElementsByClassName("myControl")[0].onmouseout = controlLeave;
//*/

$('.myControl').keydown(function (e){
	if(e.keyCode == 13){
		e.preventDefault();
		var year=$("#yearsearch").val(); //document.getElementByClass$('.myControl');
		alert(year);
		var link="http://atr.eng.utah.edu/~senguttu/drug/viz/runPred.php";
		d = new Date();
		$.ajax({
			url: link,
			type: "POST",
			data: "none",
			dataType: "html",
			success: function(data) {
				alert(data);
				window.location.href=location.href;	
			}
		});
/*
*/
	}
});

//End Slider code

    function getColor(d) {
        return d > 30000 ? '#800026' :
               d > 25000 ? '#BD0026' :
               d > 20000 ? '#E31A1C' :
               d > 15000 ? '#FC4E2A' :
               d > 10000 ? '#FD8D3C' :
               d > 5000 ? '#FEB24C' :
                         '#FED976' ;
    }

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [5000, 10000, 15000, 20000, 25000, 30000, 35000],
            labels = [],
            from, to;

        for (var i = 0; i < grades.length; i++) {
            from = grades[i];
            to = grades[i + 1];

            labels.push(
                '<i style="background:' + getColor(from + 1) + '"></i> ' +
                from + (to ? '&ndash;' + to : '+'));
        }

        div.innerHTML = labels.join('<br>');
        return div;
    };

    legend.addTo(map);
  </script>
</body>
