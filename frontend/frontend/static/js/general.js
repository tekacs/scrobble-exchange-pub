// Define global object to contain all variables/methods
var SE = SE || {};

jQuery(document).ready(function($) {
    $('.typeahead-search').typeahead({
        name: 'artists',
        remote: '../static/js/test_typeahead.json?%QUERY',
        local: ['coldplay_local', 'coldplayerz_local', 'nickelback_local', 'daft punk_local'],
        limit: 10
    });
});
