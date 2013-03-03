// TODO: make general graph drawing function, remove many lines of duplicated code
window.SE.Artist.drawMoneyGraph = function() {
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
};

window.SE.Artist.drawPointsGraph =  function() {
  'use strict';

  var Rickshaw = window.Rickshaw;

  $('#chart').empty();
  $('#legend').empty();

  var graph = new Rickshaw.Graph.Ajax( {
    element: document.getElementById("chart"),
    width: 640,
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
};

window.SE.Artist.current_price = null;
window.SE.Artist.current_guarantee = {};
window.SE.Artist.current_seconds_left = 15;
window.SE.Artist.getArtistPriceGuarantee = function(mbid) {
    var url = '/price/guarantee?artist_id=' + mbid;
    jQuery.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        complete: function(xhr, textStatus) {
            //called when complete
        },
        success: function(data, textStatus, xhr) {
            var current_timestamp = Math.round(+new Date()/1000);

            window.SE.Artist.current_guarantee = data;

            // window.SE.Artist.current_guarantee.artist.name = data.artist.name;
            // window.SE.Artist.current_guarantee.price = data.price;
            // window.SE.Artist.current_guarantee.time = data.time;
            // window.SE.Artist.current_guarantee.elephant = data.elephant;

            window.SE.Artist.current_seconds_left = data.time - current_timestamp;

            $('#buy-sell-modal .price-text').text(data.price);
            $('#buy-sell-modal .artist-text').text(data.artist.name);

            window.SE.startCountdown();

        },
        error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
        }
    });
};

window.SE.Artist.makeTransaction = function(transaction_type){
    var url = (transaction_type === 'buy') ? '/buy' : '/sell';

    jQuery.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {
            artist_id: window.SE.Artist.current_guarantee.artist.mbid,
            price: window.SE.Artist.current_guarantee.price,
            time: window.SE.Artist.current_guarantee.time,
            elephant: window.SE.Artist.current_guarantee.elephant
        },
        complete: function(xhr, textStatus) {
            //called when complete
            $('#buy-sell-modal').trigger('reveal:close');
        },
        success: function(data, textStatus, xhr) {
            //called when successful
        },
        error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
        }
    });
};

window.SE.startCountdown = function () {

    // We have reached the end of the timer, need to get a new price
    // TODO: get new price
    if (window.SE.Artist.current_seconds_left < 1){
      // get new price
      window.SE.Artist.getArtistPriceGuarantee(window.Artist.mbid);
      return;
    } else {
      window.SE.Artist.current_seconds_left = window.SE.Artist.current_seconds_left - 1;
    }

    // Reduce knob value and start a new timer
    $('#buy-sell-modal .dial').val(window.SE.Artist.current_seconds_left).trigger('change');
    $('#buy-sell-modal .timer-text').text(window.SE.Artist.current_seconds_left);
    if (window.SE.Artist.current_seconds_left <= 5){
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
      var isSelected = $(this).parent().hasClass('active');
      var field = $(this).data('chart');
      if (!isSelected){
        $(this).parent().addClass('active').siblings().removeClass('active');
        if (field === 'money') {
          window.SE.Artist.drawMoneyGraph();
        } else if (field === 'points') {
          window.SE.Artist.drawPointsGraph();
        }
      }
    });

    $('#buy-sell-modal .success').on('click', function(){
      window.SE.Artist.makeTransaction($('#buy-sell-modal .buy-sell').text());
    });

    $("#buy-button, #sell-button").click(function() {
        var elementID = $(this).attr('id');
        var subText = (elementID === 'buy-button') ? 'buy' : 'sell';
        var bgColour = (elementID === 'buy-button') ? 'auto' : '#b40200';
        var price = $(this).data('price');
        var artistname = $(this).data('artistname');

        $('#buy-sell-modal .buy-sell').text(subText);
        $('#buy-sell-modal .label').css('background-color', bgColour);

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
              window.console.log(window.SE.Artist.mbid);
              window.SE.Artist.getArtistPriceGuarantee(window.SE.Artist.mbid);
          },
          "closed": function() {
              window.clearTimeout(window.SE.price_countdown);
              $('#buy-sell-modal .dial').val(window.SE.Artist.current_seconds_left).trigger('change');
          }
        });
    });
});
