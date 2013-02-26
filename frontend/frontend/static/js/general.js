// Define global object to contain all variables/methods
var SE = SE || {};

jQuery(document).ready(function($) {
    $('.typeahead-search').typeahead({
        name: 'artists',
        remote: '../static/js/test_typeahead.json?1231awdw2aadAA23%QUERY',
        limit: 5,
        template: [
            '<div class="artist-image" style="background-image:url(\'{{img}}\')"></div>' +
            '<p class="artist-name" data-url="{{url}}">{{value}}</p>'
        ],
        engine: window.Hogan
    });

    // If we have suggestions, submitting the form takes us to the first
    // Otherwise we submit normally and go to the search results page
    $('.search-form').on('submit', function(e){
        var url, suggestions;
        suggestions = $(this).find('.tt-suggestion');
        window.console.log(suggestions);
        if (suggestions.length > 0) {
            url = $(suggestions[0]).find('p.artist-name').data('url');
            window.location.href = url;
            e.preventDefault();
            return;
        }

    });

    // TODO: fix direct search on enter key
    // WIP
    // $('.typeahead-search').on('keydown', function(e){
    //     // enter key pressed
    //     if (e.which === 13) {
    //         e.preventDefault();
    //         $(this).parents('form').first().submit();

    //     }
    // });

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

});
