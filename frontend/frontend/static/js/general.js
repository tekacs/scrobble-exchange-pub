// Define global object to contain all variables/methods
var SE = SE || {};

/* Add general functions for cookies */
window.SE.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

window.SE.csrfSafeMethod = function(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

/* Set up all unsafe ajax requests with csrf tokens */
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!window.SE.csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", window.SE.getCookie('csrftoken'));
        }
    }
});

window.SE.Search = {
    pollAddMoreLinkTimeoutSet: false,
    getMoreLink: function(query) {
        return '<li class="tt-suggestion more-link" data-value="' + query + '"><p class="artist-name" data-url="/search/?q=' + query + '">See more results for ' + query + '</p></li>';
    },
    pollAddMoreLink: function(context) {

        var parent = $($(context).parents().first());

        if (parent.find('.tt-suggestion').length > 0){

            if (parent.find('.more-link').length === 0){
                parent.find('ol.tt-suggestions').append(window.SE.Search.getMoreLink($(context).val()));
            }

            window.clearTimeout(window.SE.Search.pollAddMoreLink);
            window.SE.Search.pollAddMoreLinkTimeoutSet = false;

        } else {
            window.setTimeout(window.SE.Search.pollAddMoreLink, 50, context);
        }
    }
};

jQuery(document).ready(function($) {

    $(document).foundationAlerts();
    $(document).foundationTooltips();
    $(document).foundationTopBar();

    /* SEARCH BAR */



    // Need each to fix bug in 0.8.1: https://github.com/twitter/typeahead.js/issues/42#issuecomment-14028701
    $('.typeahead-search').each(function() {
        $(this).typeahead({
            name: 'artists',
            remote: '/search/autocomplete/?q=%QUERY',
            limit: 3,
            template: [
                '<div class="artist-image" style="background-image:url(\'{{img}}\')"></div>' +
                '<p class="artist-name" data-url="{{url}}">{{value}}</p>'
            ],
            engine: window.Hogan
        });
        // Perform initial sizing on dropdown search bar
        var width = $('.header-search').width();
        $('.header-search').find('.tt-dropdown-menu').css('width', width + 'px');
    });

    // Add more link below all suggestions
    $('.typeahead-search').on('keydown', function(e){
        if (!window.SE.Search.pollAddMoreLinkTimeoutSet){
            window.SE.Search.pollAddMoreLinkTimeoutSet = true;
            window.setTimeout(window.SE.Search.pollAddMoreLink, 50, this);
        }
    });

    $('.typeahead-search').on('keydown', function(e){
        // enter key pressed, submit
        if (e.which === 13) {
            $(this).parents('form').first().submit();
        }
    });

    // Change lucky status to false when on more items link
    $('.typeahead-search').on('keyup', function(e){
        var parent = $($(this).parents().first());
        var selectedItem = parent.find('.tt-is-under-cursor');

        if ($(selectedItem).hasClass('more-link')){
            $(parent).parents().find('.lucky-hidden').val('false');
        } else {
            $(parent).parents().find('.lucky-hidden').val('true');
        }
    });

    // Clicking an artist name takes us to their page
    $(document).on('click', '.tt-suggestion', function(e){
        var url = $(this).find('p.artist-name').data('url');
        window.location.href = url;
    });


    // Highlight first suggestion by default - see visited css class
    // Had to do this due to lack of events or callbacks in typeahead 0.8.1
    $(document).on('focus keydown', '.typeahead-search', function(e){
        $('ol.tt-suggestions li.tt-suggestion:first-child').addClass('visited');
    });
    $(document).on('focus', '.typeahead-search', function(e){
        $('ol.tt-suggestions li.tt-suggestion:first-child').addClass('tt-is-under-cursor');
    });
    $(document).on('mouseover', 'ol.tt-suggestions li.tt-suggestion', function(){
        $($(this).parents().first()).find('li.tt-suggestion:first-child').addClass('visited');
    });


    $(window).resize(function() {
        var width = $('.header-search').width();
        $('.header-search').find('.tt-dropdown-menu').css('width', width + 'px');
    });


    /* TROPHY CONTROL */

    $('.see-more-trophies').on('click', function(e){
        $('.trophy').removeClass('hidden');
        $(this).hide();
    });



});
