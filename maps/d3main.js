function initalizeBaseMap(mapCtrl){
  var map = new L.map(mapCtrl.id).setView([40.757668, -73.978711], 12)
  .addLayer(new L.TileLayer("http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png"));
  return map;  
}

function setMap(srcJson, mapCtrl, baseMap){
  var width = mapCtrl.width;
  var height = mapCtrl.height;

  var map = baseMap;

  var svg = d3.select(map.getPanes().overlayPane).append("svg"),
  g = svg.append("g").attr("class", "leaflet-zoom-hide");

  d3.json(srcJson, function(error, jsonData) {
    if (error) throw error;
	var attName = "GRIDCODE"
    //add geometry to map
    var transform = d3.geo.transform({point: projectPoint}),
    path = d3.geo.path().projection(transform);

    // var recolorMap = colorScale(jsonData.features);

    var counties = g.selectAll("path")
    .data(jsonData.features)
    .enter().append("path").attr("class", function(d){
		if(d.properties[attName] == 1) return "counties firstClass";
		else return "counties";
	}) //assign class for styling
    .attr("id", function(d) {
      return d.properties.FIPS })
    .attr("d", path) //project data as geometry in svg
    .style("fill", function(d) { //color enumeration units
      return choropleth(d);
    });

    map.on("viewreset", reset);
    reset();

    // Reposition the SVG to cover the features.
    function reset() {
      var bounds = path.bounds(jsonData),
      topLeft = bounds[0],
      bottomRight = bounds[1];

      svg.attr("width", bottomRight[0] - topLeft[0])
      .attr("height", bottomRight[1] - topLeft[1])
      .style("left", topLeft[0] + "px")
      .style("top", topLeft[1] + "px");

      g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");

      counties.attr("d", path);
    }

    // Use Leaflet to implement a D3 geometric transformation.
    function projectPoint(x, y) {
      var point = map.latLngToLayerPoint(new L.LatLng(y, x));
      this.stream.point(point.x, point.y);
    }

	function choropleth(d){
	  var colorOrder = ["#ffffb2",
		"#fed976",
		"#feb24c",
		"#fd8d3c",
		"#fc4e2a",
		"#e31a1c",
		"#b10026"]
	  //get data value
	  var value = d.properties[attName];
	  //if value exists, assign it a color; otherwise assign gray
	  if (value) {
		return colorOrder[value - 1]; //recolorMap holds the colorScale generator
	  } else {
		return "#ccc";
	  }
	}
  });
}
