window.SE.Leaderboards = {
    options: {
        "aoColumns" : [ {sTitle : "Rank"}, {sTitle : "User"}, {sTitle : "Score"}],
        'bDeferRender': true,
        'sDom': '<"H"r>t<"F"iS>',
        'sScrollY': '800px',
        'bPaginate': true,
        'bSort': false,
        'bScrollCollapse': true,
        'bStateSave': true,
        "fnServerData": function( sUrl, aoData, fnCallback, oSettings ) {
            oSettings.jqXHR = $.ajax( {
                "url": sUrl,
                "data": aoData,
                "success": fnCallback,
                "dataType": "jsonp",
                "cache": true
            } );
        },
        'fnInitComplete': function () {
            this.fnAdjustColumnSizing();
            var currentLeagueSelected = window.SE.Leaderboards.getSelectedLeague();
            if (currentLeagueSelected === window.SE.User.league){
                window.SE.Leaderboards.scrollToName(this);
            }
        }
    },

    // default timespan 2, for a week
    current_timespan: 2,

    leaderboards: [],

    scrollToName: function(leaderboard) {
        // Scroll to arbitrary position above the user's name
        if (window.SE.User.leaderboard_position){
            leaderboard.fnSettings().oScroller.fnScrollToRow( window.SE.User.leaderboard_position - 6 );
        }
    },

    scrollToNameHandler: function() {
        var currentLeagueSelected = window.SE.Leaderboards.getSelectedLeague();
        var currentLeaderboard = window.SE.Leaderboards.leaderboards[currentLeagueSelected];
        if (currentLeagueSelected === window.SE.User.league){
            window.SE.Leaderboards.scrollToName(currentLeaderboard);
        }
    },

    // Returns uid of league selected
    getSelectedLeague: function() {
        return $('ul.leaderboards li.active table.leaderboard').first().data('leagueuid');
    },

    updatePageForTimespan: function(newTimespan) {
        if (window.SE.Leaderboards.current_timespan === newTimespan){
            return;
        }

        window.SE.Leaderboards.current_timespan = newTimespan;
        var name, sourceData;
        switch(newTimespan){
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
                name = 'Last Day';
                break;
        }

        $('span.leaderboards-time').text(name);
    },

    createTable: function(leagueUid, timespan) {
        var newOptions = window.SE.Leaderboards.options;
        newOptions.bDestroy = true;
        newOptions.sAjaxSource = '/leaderboards/get/?league_id=' + leagueUid + '&time_range=' + timespan;
        window.SE.Leaderboards.leaderboards[leagueUid] = $('table[data-leagueuid=' + leagueUid + ']').dataTable(newOptions);
    },

    createAppropriateTable: function() {
        var currentLeague = window.SE.Leaderboards.getSelectedLeague();
        window.SE.Leaderboards.createTable(currentLeague, window.SE.Leaderboards.current_timespan);
    },

    // Update the information on the sidebar via Ajax to keep consistent with currently selected timespan
    getContextualUserData: function() {
        if (!window.SE.User.username){
            return;
        }
        var timespan = window.SE.Leaderboards.current_timespan;
        var url = '/leaderboards/get/user/?time_range=' + timespan;
        var league, position, points, rival_name, rival_points;
        jQuery.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function(data, textStatus, xhr) {
            league = data.user_league.name;
            position = data.user_position;
            points = data.user_points;
            rival_name = data.next_user.name;
            rival_points = data.next_user.points;

            window.SE.User.league = league;
            window.SE.User.leaderboard_position = position;

            $('.context-user-league').text(league);
            $('.context-user-position').text(position);
            $('.context-user-points').text(points);
            $('.context-next_user-name').text(rival_name);
            $('.context-next_user-points').text(rival_points);
          }
        });

    }
};

$(document).ready(function() {
    $(document).foundationAccordion();

    window.SE.Leaderboards.getContextualUserData();
    window.SE.Leaderboards.createAppropriateTable();

    // Scroll to the correct position in the table (to the user's name)
    $('ul.leaderboards li').on('opened', window.SE.Leaderboards.scrollToNameHandler);

    // Re-adjust column sizing upon window resize
    $(window).resize(function() {
        var leagueUid = window.SE.Leaderboards.getSelectedLeague();
        window.SE.Leaderboards.leaderboards[leagueUid].fnAdjustColumnSizing();
    });

    // Fix bug where columns would be messed up when switching
    // 'opened' triggered by jquery.foundation.accordion.custom.js, not in vanilla
    $('ul.leaderboards li').on('opened', function(){
        if (!window.SE.Leaderboards.leaderboards[window.SE.Leaderboards.getSelectedLeague()]){
            window.SE.Leaderboards.createAppropriateTable();
        }
        var leagueUid = $(this).find('table.leaderboard').data('leagueuid');
        window.SE.Leaderboards.leaderboards[leagueUid].fnAdjustColumnSizing();
    });

    $('a.time-adjust').on('click', function() {
        var timespan = $(this).data('timeadjust');

        window.SE.Leaderboards.updatePageForTimespan(timespan);

        window.SE.Leaderboards.current_timespan = timespan;

        $('a.time-adjust').removeClass('selected');
        $(this).addClass('selected');

        window.SE.Leaderboards.leaderboards = [];

        window.SE.Leaderboards.createAppropriateTable();
        window.SE.Leaderboards.getContextualUserData();

    });

});
