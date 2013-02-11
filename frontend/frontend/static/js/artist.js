// Very rough and ready approach to handling the JS on artists' pages
var Artist = {
    name: '',
    id: '',

    drawGraph: function() {
        'use strict';

        //set up our data series with 50 random data points
        var Rickshaw = window.Rickshaw;

        var seriesData = [ [] ];
        var random = new Rickshaw.Fixtures.RandomData(60);

        for (var i = 0; i < 60; i++) {
          random.addData(seriesData);
        }

        var graph = new Rickshaw.Graph( {
          element: document.getElementById("lineChart"),
          width: 620,
          height: 300,
          renderer: 'area',
          stroke: true,
          series: [
            {
              color: "#eee",
              stroke: "#0187c5",
              data: seriesData[0],
              name: 'Price for ' + this.name
            }
          ]
        } );

        var hoverDetail = new Rickshaw.Graph.HoverDetail({graph: graph});
        var x_axis = new Rickshaw.Graph.Axis.Time({graph: graph });

        graph.render();
    }
};
