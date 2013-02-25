// Very rough and ready approach to handling the JS on artists' pages
window.SE.Artist = {
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

window.SE.startCountdown = function () {
    var seconds = $('.dial').val();

    // We have reached the end of the timer, need to get a new price
    // TODO: get new price
    seconds = (seconds < 1) ? 15 : seconds - 1;

    // Reduce knob value and start a new timer
    $('.dial').val(seconds).trigger('change');
    $('.timer-text').text(seconds);
    if (seconds <= 5){
        $('.dial').trigger(
            'configure',
            {
                'fgColor': '#b40200',
                'inputColor': '#b40200'
            }
        );
    } else {
        $('.dial').trigger(
            'configure',
            {
                'fgColor': '#0187c5',
                'inputColor': '#0187c5'
            }
        );
    }
    window.SE.price_countdown = setTimeout(window.SE.startCountdown, 1000);
};

jQuery(document).ready(function($) {
  $("#buy-button, #sell-button").click(function() {
      var elementID = $(this).attr('id');
      var subText = (elementID === 'buy-button') ? 'buy' : 'sell';
      var bgColour = (elementID === 'buy-button') ? 'auto' : '#b40200';
      var price = $(this).data('price');
      var artistname = $(this).data('artistname');

      $('.buy-sell').text(subText);
      $('.label').css('background-color', bgColour);
      $('#buy-sell-modal .price-text').text(price);
      $('#buy-sell-modal .artist-text').text(artistname);

      $("#buy-sell-modal").reveal({
          // Order of function calls for knob:
          // open -> opened -> close -> closed
          "open": function() {
              $('.dial').knob().trigger(
                  'configure',
                  {
                      'fgColor': '#0187c5',
                      'inputColor': '#0187c5'
                  }
              );
          },
          "opened": function() {
              window.SE.startCountdown();
          },
          "closed": function() {
              clearTimeout(window.price_countdown);
              $('.dial').val(15).trigger('change');
          }
      });
  });
});
