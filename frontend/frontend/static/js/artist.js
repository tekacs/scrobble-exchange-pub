// Very rough and ready approach to handling the JS on artists' pages
var Artist = {
    name: '',
    id: '',

    drawGraph: function() {
        'use strict';

        //set up our data series with 50 random data points
        var Rickshaw = window.Rickshaw;

        var artistPriceData = [ [] ];
        var artistDividendData = [ [] ];
        var random = new Rickshaw.Fixtures.RandomData(60);

        for (var i = 0; i < 60; i++) {
          random.addData(artistPriceData);
          random.addData(artistDividendData);
        }

        var graph = new Rickshaw.Graph( {
          element: document.getElementById("priceChart"),
          width: 620,
          height: 300,
          renderer: 'line',
          stroke: true,
          series: [
            {
              color: "#dc1303",
              stroke: "",
              data: artistPriceData[0],
              name: 'Price for ' + this.name
            }, {
              color: "#0187c5",
              stroke: "#0187c5",
              data: artistDividendData[0],
              name: 'Dividends for ' + this.name
            }
          ]
        } );

        var hoverDetail = new Rickshaw.Graph.HoverDetail({graph: graph});
        var x_axis = new Rickshaw.Graph.Axis.Time({graph: graph });

        graph.render();
    }
};
