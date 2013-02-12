// TODO: set up object to contain settings such as this
var price_countdown;

function startCountdown() {
    var seconds = $('.dial').val();

    // We have reached the end of the timer, need to get a new price
    // TODO: get new price
    seconds = (seconds < 1) ? 15 : seconds - 1;
    
    // Reduce knob value and start a new timer
    $('.dial').val(seconds).trigger('change');
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
    price_countdown = setTimeout(startCountdown, 1000);
}

$(document).ready(function() {
    $("#buy-button, #sell-button").click(function() {
        var elementID = $(this).attr('id');
        var subText = (elementID === 'buy-button') ? 'buy' : 'sell';

        $('.buy-sell').text(subText);

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
                startCountdown();
            },
            "closed": function() {
                clearTimeout(window.price_countdown);
                $('.dial').val(15).trigger('change');
            }
        });
    });
});


