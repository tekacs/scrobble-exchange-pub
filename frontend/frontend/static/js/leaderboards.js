window.SE.Leaderboards = {
    options: {
        // time_range = 2, last week
        //'sAjaxSource': '/leaderboards/get/?league_id=1&time_range=2',
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
                window.SE.Leaderboards.scrollToName(this);
            }
        }
    },

    current_timespan: 2,

    leaderboards: [],

    scrollToName: function(leaderboard) {
        // Scroll to arbitrary position above the user's name
        leaderboard.fnSettings().oScroller.fnScrollToRow( window.SE.User.leaderboard_position - 6 );
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

    switchAllDataSources: function(newTimespan) {

        var newOptions = window.SE.Leaderboards.options;

        // Destroy old table on new construction
        newOptions.bDestroy = true;

        var leagueCount = 0, newSource, leagueUid;
        $('table.leaderboard[id^="DataTables_"]').each(function(){
            leagueUid = $(this).data('leagueuid');
            newOptions.sAjaxSource = '/leaderboards/get/?league_id=' + leagueUid + '&time_range=' + newTimespan;
            $(this).dataTable(newOptions);
        });
    },

    // Update the information on the sidebar via Ajax to keep consistent with currently selected timespan
    getContextualUserData: function(timespan) {
        var url = '/leaderboards/get/user/?time_range=' + timespan;
        var league, position, points, rival_name, rival_points;
        jQuery.ajax({
          url: url,
          type: 'GET',
          dataType: 'json',
          success: function(data, textStatus, xhr) {
            league = data.user_league.name;
            //position = data.user_position;
            position = 2;
            points = data.user_points;
            rival_name = data.next_user.name;
            rival_points = data.next_user.points;

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

    window.SE.Leaderboards.getContextualUserData(window.SE.Leaderboards.current_timespan);

    $('table.leaderboard').each(function(){
        var leagueUid = $(this).data('leagueuid');
        window.SE.Leaderboards.options.sAjaxSource = '/leaderboards/get/?league_id=' + leagueUid + '&time_range=2',
        window.SE.Leaderboards.leaderboards[leagueUid] = $(this).dataTable(window.SE.Leaderboards.options).fadeIn();
    });

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
        var leagueUid = $(this).find('table.leaderboard').data('leagueuid');
        window.SE.Leaderboards.leaderboards[leagueUid].fnAdjustColumnSizing();
    });

    $('a.time-adjust').on('click', function() {
        var timespan = $(this).data('timeadjust');

        $('a.time-adjust').removeClass('selected');
        $(this).addClass('selected');


        window.SE.Leaderboards.updatePageForTimespan(timespan);
        window.SE.Leaderboards.switchAllDataSources(timespan);
        window.SE.Leaderboards.getContextualUserData(timespan);

    });

});
