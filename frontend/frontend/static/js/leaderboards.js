window.SE.Leaderboards = {
    options: {
        'sAjaxSource': '/leaderboards/get/?league_id=1&time_range=0',
        "aoColumns" : [ {sTitle : "Rank"}, {sTitle : "User"}, {sTitle : "Score"}],
        'bDeferRender': true,
        'sDom': '<"H"fr>t<"F"iS>',
        'sScrollY': '800px',
        'bJQueryUI': true,
        'bPaginate': true,
        'bSort': false,
        'bScrollCollapse': true,
        'bStateSave': true,
        'fnInitComplete': function () {
            this.fnAdjustColumnSizing();
            var currentLeagueSelected = window.SE.Leaderboards.getSelectedLeague();
            if (currentLeagueSelected === window.SE.User.league){
                //window.SE.Leaderboards.scrollToNameHandler();
                window.SE.Leaderboards.scrollToName(this);
            }
        }
    },

    current_timespan: 0,

    leaderboards: [],
    needFixing: [true, true, true],
    adjustColummnsHandler: function() {
        // Fixes problem with column headings displaying incorrectly
        // When a tab is changed, adjust column sizing, but only once for each leaderboard
        window.console.log(window.SE.Leaderboards);
        // Hash of #leagueX where X is the league number
        var league = parseInt(window.location.hash[window.location.hash.length - 1], 10);

        // indexes 0-based
        var index =  league - 1;

        if (window.SE.Leaderboards.needFixing[index]){
            window.SE.Leaderboards.leaderboards[index].fnAdjustColumnSizing();
            window.SE.Leaderboards.needFixing[index] = false;
        }

        var numberFixed = 0;
        for (var i = 0; i < window.SE.Leaderboards.leaderboards.length; i++){
            if (window.SE.Leaderboards.needFixing[i] === false){
                numberFixed = numberFixed + 1;
            }
        }

        if (numberFixed === window.SE.Leaderboards.leaderboards.length){
            $(window).off('hashchange', window.SE.Leaderboards.adjustColummnsHandler);
        }
    },

    scrollToName: function(leaderboard) {
        // Scroll to arbitrary position above the user's name
        leaderboard.fnSettings().oScroller.fnScrollToRow( window.SE.User.leaderboard_position - 6 );
    },

    scrollToNameHandler: function() {
        var currentLeagueSelected = window.SE.Leaderboards.getSelectedLeague();
        var currentLeaderboard = window.SE.Leaderboards.leaderboards[currentLeagueSelected-1];
        if (currentLeagueSelected === window.SE.User.league){
            window.SE.Leaderboards.scrollToName(currentLeaderboard);
        }
    },

    getSelectedLeague: function() {
        var hash = window.location.hash;
        // Hash of #leagueX where X is the league number, or 1 if on default page
        return (hash) ? parseInt(hash[hash.length - 1], 10) : 1;
    },

    switchAllDataSources: function(newSources) {

        var newOptions = window.SE.Leaderboards.options;
        //newOptions.sAjaxSource = newSource;
        //newOptions.sAjaxSource = '../static/js/test_data_leaderboards.json';
        // Destroy old table on new construction
        newOptions.bDestroy = true;

        for (var i = window.SE.Leaderboards.leaderboards.length - 1; i >= 0; i--) {
            newOptions.sAjaxSource = newSources[i];
            $(window.SE.Leaderboards.leaderboards[i]).dataTable(newOptions);
        }

        // Restart handler to fix column problems after new data loaded
        window.SE.Leaderboards.needFixing = [true, true, true];
        $(window).on('hashchange', window.SE.Leaderboards.adjustColummnsHandler);
    }
};

$(document).ready(function() {
    $(document).foundationTabs();

    window.SE.Leaderboards.leaderboards[0] = $('.leaderboard-1').dataTable(window.SE.Leaderboards.options).fadeIn();
    window.SE.Leaderboards.leaderboards[1] = $('.leaderboard-2').dataTable(window.SE.Leaderboards.options).fadeIn();
    window.SE.Leaderboards.leaderboards[2] = $('.leaderboard-3').dataTable(window.SE.Leaderboards.options).fadeIn();

    $(window).on('hashchange', window.SE.Leaderboards.adjustColummnsHandler);
    $(window).on('hashchange', window.SE.Leaderboards.scrollToNameHandler);

    // Re-adjust column sizing upon window resize
    $(window).resize(function() {
        var league = window.SE.Leaderboards.getSelectedLeague();
        window.SE.Leaderboards.leaderboards[league - 1].fnAdjustColumnSizing();
    });

    $('a.time-adjust').on('click', function() {
        var timespan = $(this).data('timeadjust');

        if (window.SE.Leaderboards.current_timespan === timespan){
            return false;
        }

        window.SE.Leaderboards.current_timespan = timespan;
        var name, sourceData;
        switch(timespan){
            case(0):
                name = 'All Time';
                break;
            case(1):
                name = 'Last Month';
                break;
            case(2):
                name = 'Last Week';
                break;
            case(3):
                name = 'Last 24 Hours';
                break;
        }

        $('a.time-adjust').removeClass('selected');
        $(this).addClass('selected');
        $('span.leaderboards-time').text(name);

        var newSources = [];
        newSources[0] = '/leaderboards/get/?league_id=1&time_range=' + timespan;
        newSources[1] = '/leaderboards/get/?league_id=2&time_range=' + timespan;
        newSources[2] = '/leaderboards/get/?league_id=3&time_range=' + timespan;

        window.SE.Leaderboards.switchAllDataSources(newSources);

    });

});
