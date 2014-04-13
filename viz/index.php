<!DOCTYPE HTML>
<head>
  <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" />
  <link rel="stylesheet" href="style.css" />
  <script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script>
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
