window.SE.Artist = {
    // TODO: reduce repeated code, make more general
    drawMoneyGraph: function() {
        'use strict';
        var Rickshaw = window.Rickshaw;

        $('#chart').empty();
        $('#legend').empty();

        var graph = new Rickshaw.Graph.Ajax( {
          element: document.getElementById("chart"),
          width: 620,
          height: 300,
          renderer: 'line',
          dataURL: '/artist/history/?artist_id=' + window.SE.Artist.mbid + '&days=7&field=money',
          series: [
            {
              color: "#dc1303",
              name: 'price'
            }, {
              color: "#0187c5",
              name: 'dividends'
            }
          ],
          onComplete: function(transport) {
            var graph = transport.graph;

            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: graph,
                formatter: function(series, x, y) {
                    return (series.name === 'price') ? 'Market price: $' + y : 'Dividends: $' + y;
                }
            });

            var yAxis = new Rickshaw.Graph.Axis.Y({
                graph: graph,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT
            });

            var time = new Rickshaw.Fixtures.Time();
            var days = time.unit('day');

            var xAxis = new Rickshaw.Graph.Axis.Time({
                graph: graph,
                timeUnit: days
            });

            var legend = new Rickshaw.Graph.Legend({
                graph: graph,
                element: document.querySelector('#legend')
            });

            var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
                graph: graph,
                legend: legend
            });

            var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
                graph: graph,
                legend: legend
            });

            graph.update();

            $('.rickshaw_legend span.label').each(function(){
                if ($(this).text() === 'dividends'){
                    $(this).html('Dividends <strong>($)</strong>');
                } else if ($(this).text() === 'price'){
                    $(this).html('Market price <strong>($)</strong>');
                }
            });
          }
        });
    },
    drawPointsGraph: function() {
        'use strict';

        var Rickshaw = window.Rickshaw;

        $('#chart').empty();
        $('#legend').empty();

        var graph = new Rickshaw.Graph.Ajax( {
          element: document.getElementById("chart"),
          width: 620,
          height: 300,
          renderer: 'line',
          dataURL: '/artist/history/?artist_id=' + window.SE.Artist.mbid + '&days=7&field=points',
          series: [
            {
              color: "#dc1303",
              name: 'points'
            }
          ],
          onComplete: function(transport) {
            var graph = transport.graph;

            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: graph,
                formatter: function(series, x, y) {
                    return 'Points: ' + y;
                }
            });

            var yAxis = new Rickshaw.Graph.Axis.Y({
                graph: graph,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT
            });

            var time = new Rickshaw.Fixtures.Time();
            var days = time.unit('day');

            var xAxis = new Rickshaw.Graph.Axis.Time({
                graph: graph,
                timeUnit: days
            });

            var legend = new Rickshaw.Graph.Legend({
                graph: graph,
                element: document.querySelector('#legend')
            });

            var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
                graph: graph,
                legend: legend
            });

            var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
                graph: graph,
                legend: legend
            });

            graph.update();

            $('.rickshaw_legend span.label').each(function(){
                $(this).html('Points');
            });
          }
        });
    }
};

window.SE.startCountdown = function () {
    var seconds = $('.dial').val();

    // We have reached the end of the timer, need to get a new price
    // TODO: get new price
    seconds = (seconds < 1) ? 15 : seconds - 1;

    // Reduce knob value and start a new timer
    $('#buy-sell-modal .dial').val(seconds).trigger('change');
    $('#buy-sell-modal .timer-text').text(seconds);
    if (seconds <= 5){
        $('#buy-sell-modal .dial').trigger(
            'configure',
            {
                'fgColor': '#b40200',
                'inputColor': '#b40200'
            }
        );
    } else {
        $('#buy-sell-modal .dial').trigger(
            'configure',
            {
                'fgColor': '#0187c5',
                'inputColor': '#0187c5'
            }
        );
    }
    window.SE.price_countdown = window.setTimeout(window.SE.startCountdown, 1000);
};

jQuery(document).ready(function($) {

    window.SE.Artist.drawMoneyGraph();

    $('a.chart-switch').on('click', function(){
      var isSelected = $(this).hasClass('selected');
      var field = $(this).data('chart');
      if (!isSelected){
        $(this).addClass('selected').siblings().removeClass('selected');
        if (field === 'money') {
          window.SE.Artist.drawMoneyGraph();
        } else if (field === 'points') {
          window.SE.Artist.drawPointsGraph();
        }
      }
    });

    $("#buy-button, #sell-button").click(function() {
        var elementID = $(this).attr('id');
        var subText = (elementID === 'buy-button') ? 'buy' : 'sell';
        var bgColour = (elementID === 'buy-button') ? 'auto' : '#b40200';
        var price = $(this).data('price');
        var artistname = $(this).data('artistname');

        $('#buy-sell-modal .buy-sell').text(subText);
        $('#buy-sell-modal .label').css('background-color', bgColour);
        $('#buy-sell-modal .price-text').text(price);
        $('#buy-sell-modal .artist-text').text(artistname);

        $("#buy-sell-modal").reveal({
          // Order of function calls for knob:
          // open -> opened -> close -> closed
          "open": function() {
              $('#buy-sell-modal .dial').knob().trigger(
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
              window.clearTimeout(window.SE.price_countdown);
              $('#buy-sell-modal .dial').val(15).trigger('change');
          }
        });
    });
});
