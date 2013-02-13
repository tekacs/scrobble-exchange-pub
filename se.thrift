## Scrobble-Exchange Thrift Definitions

## Interface definitions

namespace py se_api

## API version
# Format: Major/Minor/Patch
# Major is for backwards-incompatible changes
# Minor is for backwards-compatible ones (e.g. adding optional parameters)
# Patch is for small bugfixes and similar

const string VERSION = "1.0.0"

## Structs

# Auth

# Artist

/** Basic artist info. imgurls is a mapping from size to location. Optionally 
    includes whether a predetermined user owns this artist or not */
struct Artist {
    1: required string mbid
    2: optional string name
    3: optional map<string,string> imgurls
}

/** Ordered list by date of artist values (oldest to newest). Formatted as 
    (date,price) pairs.
    Daterange might help in drawing the graphs (?) */
struct ArtistHistory {
    1: required list<map<i32,i32>> histvalue
    2: optional i32 daterange
}

/** Encapsulates the data in our db. num_remaining is the amount available to 
    be bought */ 
struct ArtistSE {
    1: required Artist artist
    2: required i32 price
    3: required i32 num_remaining
    4: optional bool ownedby
}

/** Encapsulates the data from last.fm's artist.getInfo. */
struct ArtistLFM {
    1: required Artist artist
    2: required bool streamable
    3: required i32 listeners
    4: required i32 plays
    5: required list<string> tags
    6: required list<Artist> similar
    7: required string bio
}

# User

/** A single purchase/sale. Time is when the trade occurred. */
struct Trade {
    1: required Artist artist
    2: required i32 price
    3: required i32 time
}

/** User trophies. Challenge is a possible arbitrary `difficulty to obtain' 
    measurement, and is most likely not returned. */
struct Trophy {
    1: required string name
    2: required string description
    3: optional string challenge
}

/** Basic user info. */
struct User {
    1: required string name
}

/** Basic authenticated user. Does not necessarily include their money */
struct AuthUser {
    1: required string name
    2: required string session_key
    3: optional i32 money
}

/** Encapsulates all the user data. For a new user: trades, stocks and trophies 
    will be empty lists. */
struct UserData {
    1: required User user
    2: required list<Trade> trades
    3: required list<ArtistSE> stocks
    4: required list<Trophy> trophies
    5: optional i32 curleaguepos
}

/** Contains a list of users in decreasing leaderboard position. Position is 
    the place of the current user in that leaderboard. */
struct UserLeaderboard {
    1: required list<User> users
    2: optional i32 position
}

# Transaction

/** Encapsulates the guarantee for purchase/sale that is provided to the user. 
    Elephant is the generated token that is first sent and then returned. */
struct Guarantee {
    1: required string elephant
    2: required i32 value
    3: required i32 time
}

## Exceptions
# These really need to be filled out with all of the actual errors that could 
# occur.

enum LoginCode {
    AUTH = 1,
    ACC = 2,
    CONN = 3,
}

exception LoginException {
    1: required LoginCode code
    2: required string message
}

enum SearchCode {
    NONE = 1,
    CONN = 2,
    ARG = 3
}

exception SearchException {
    1: required SearchCode code
    2: required string message
}

enum TransactionCode {
    NONE = 1,
    CONN = 2,
    NUM = 3
}

exception TransactionException {
    1: required TransactionCode code
    2: required string message
}

enum UserCode {
    NONE = 1,
    CONN = 2
}

exception UserException {
    1: required UserCode code
    2: required string message
}

## Service definition

service ScrobbleExchange {
   
    # Login
    
    /** Returns the SE API key for sending to last.fm */
    string apikey (),
    
    /** If successful, returns the user session token. */
    string login(1: required string username, 2: required string token) throws 
(1: LoginException lexp),
    
    # Data retrieval
    # Artists
    
    /** Returns basic artist info. If either the artist or the mbid is unknown, 
        then the empty string should be sent. */
    Artist getArtist (1: required Artist artist) throws (1: SearchException 
searchexp),
    
    /** Returns only MBID and name. If either artist or mbid are unknown, then 
        the empty string should be sent */
    Artist getLightArtist (1: required Artist artist) throws (1: 
SearchException searchexp),
    
    /** Returns the data from our db. If the artist isn't there, the data gets 
        on-demand pulled. If either artist or mbid are unknown, then the empty 
        string should be sent. */
    ArtistSE getArtistSE (1: required Artist artist) throws (1: SearchException 
searchexp),
    
    /** Returns the artist info from last.fm for the artist. If either artist 
        or mbid are unknown, then the empty string should be sent. */
    ArtistLFM getArtistLFM (1: required Artist artist) throws (1:SearchException 
searchexp),

    /** Returns a list of tuples of the price of the artist over time. For new 
        artists the empty list is returned. */
    ArtistHistory getArtistHistory (1: required Artist artist) throws (1: 
SearchException searchexp),
    
    /** returns a list of possible artists from a partial string. Ordered by 
        decreasing relevance. List size is limited to 5 elements. */
    list<Artist> searchArtist (1: required string text) throws (1: 
SearchException searchexp),
    
    /** Returns a list of the n top artists by decreasing value. By default, 
        tag should be the empty string, and only used if you want specific tag 
        access. */
    list<Artist> getTopArtists (1: required i32 n, 2: string tag),
    
    /** Returns a list of the n most traded artists by decreasing value. */
    list<Artist> getTradedArtists (1: required i32 n),
    
    /** Returns a list of the n most recent trades */
    list<Artist> getRecentTrades (1: required i32 n)
    
    # User
   
    /** Returns extended user data for the current user. Requires the authuser 
        token for validation */
    UserData getUserData (1: required AuthUser user) throws (1: UserException 
uexp),
    
    /** Returns the n top users by decreasing value in the given league. */
    UserLeaderboard getTopUsers (1: required i32 n, 2: required string league) 
throws (1: UserException uexp),
    
    /** Returns a list of 10 users with 4 above and 5 below in the leaderboard 
        compared to the user provided, including the user's position. Requires 
        the session token for validation */
    UserLeaderboard getNearUsers (1: required AuthUser user) throws (1: 
UserException uexp),
    
    # Data Modification
    
    /** Returns the guarantee token (elephant) to the front end */
    Guarantee getGuarantee (1: required Artist artist) throws (1: 
TransactionException transexp),
    
    /** Buys artist for user, and returns the new value of that stock in the 
        game. */
    i32 buyArtist (1: required Guarantee transaction, 2: required AuthUser 
user) throws (1: TransactionException transexp),
    
    /** Sells artist for user, and returns the new value of that artist. */
    i32 sellArtist (1: required Guarantee transaction, 2: required AuthUser 
user) throws (1: TransactionException transexp)
   
}
