## Scrobble-Exchange Thrift Definitions

## Interface definitions

namespace py se_api

## API version
# Format: Major/Minor/Patch
# Major is for backwards-incompatible changes
# Minor is for backwards-compatible ones (e.g. adding optional parameters)
# Patch is for small bugfixes and similar

const string VERSION = "2.0.0"

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
    (date,price) pairs. */
struct ArtistHistory {
    1: required list<map<i32,i32>> histvalue
}

/** Artist biography object */
struct ArtistBio {
    1: required string summary
    2: required string content
}

/** Encapsulates the data in our db. num_remaining is the amount available to 
    be bought. Price will be either the buy price or sell price */ 
struct ArtistSE {
    1: required Artist artist
    2: required i32 price
    3: required i32 numremaining
    4: required i32 points
    5: required i32 dividend
    6: optional bool ownedby
}

/** Encapsulates the data from last.fm's artist.getInfo. */
struct ArtistLFM {
    1: required Artist artist
    2: required bool streamable
    3: required i32 listeners
    4: required i32 plays
    5: required list<string> tags
    6: optional list<Artist> similar
    7: required ArtistBio bio
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

/** User leagues. */
struct League {
    1: required string name
    2: optional string description
    3: optional string icon
}

/** Basic user info. */
struct User {
    1: required string name
    2: optional i32 points
    3: optional string profileimage
}

/** Basic authenticated user. Does not necessarily include their money */
struct AuthUser {
    1: required User name
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
    5: required League league
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
    2: required Artist artist
    3: required i32 price
    4: required i32 time
}

## Exceptions

/** Transient errors, which may disappear on a retry **/
exception TransientError {
    1: required string message
}

/** Authentication-related errors, such as needing to reauthenticate **/
exception AuthenticationError {
    1: required string message
}

/** Data errors, meaning invalid data was passed to the API **/
exception DataError {
    1: required string message
}

/** Programming errors, meaning something is wrong in the application **/
exception ProgrammingError {
    1: required string message
}

/** Service errors, issues with connections that shouldn't be retried **/
exception ServiceError{
    1: required string message
}

## Service definition

service ScrobbleExchange {
   
    # Login
    
    /** Returns the SE API key for sending to last.fm */
    string apikey (),
    
    /** If successful, returns the AuthUser with the user session token */
    AuthUser login(1: required string token) throws (1: TransientError t, 2: 
AuthenticationError a, 3: DataError d, 4: ProgrammingError p, 5: ServiceError 
s),
    
    # Data retrieval
    # Artists
    
    /** Returns basic artist info. If either the artist or the mbid is unknown, 
        then the empty string should be sent. */
    Artist getArtist (1: required Artist artist) throws (1: TransientError t, 2: 
AuthenticationError a, 3: DataError d, 4: ProgrammingError p, 5: ServiceError 
s),
    
    /** Returns only MBID and name. If either artist or mbid are unknown, then 
        the empty string should be sent */
    Artist getLightArtist (1: required Artist artist) throws (1: TransientError 
t, 2:AuthenticationError a, 3: DataError d, 4: ProgrammingError p, 5: 
ServiceError s),
    
    /** Returns the data from our db. If the artist isn't there, the data gets 
        on-demand pulled. If either artist or mbid are unknown, then the empty 
        string should be sent. User sets the `ownedby' bool, by default it 
        should be an empty string the name */
    ArtistSE getArtistSE (1: required Artist artist, 2: required User user) 
throws (1: TransientError t, 2: AuthenticationError a, 3: DataError d,4: 
ProgrammingError p, 5: ServiceError s),
    
    /** Returns the artist info from last.fm for the artist. If either artist 
        or mbid are unknown, then the empty string should be sent. An 
        authenticated user is required to return recommended artists, otherwise 
        the parameter should be set to none */
    ArtistLFM getArtistLFM (1: required Artist artist, 2: required AuthUser 
user) throws (1: TransientError t, 2: AuthenticationError a, 3: DataError d, 4: 
ProgrammingError p, 5: ServiceError s),

    /** Returns a list of tuples of the price of the artist the past n days. 
        For new artists the empty list is returned. */
    ArtistHistory getArtistHistory (1: required Artist artist, 2: required i32 
n) throws (1: TransientError t, 2: AuthenticationError a, 3: DataError d, 4: 
ProgrammingError p, 5: ServiceError s),
    
    /** returns a list of possible artists from a partial string. Ordered by 
        decreasing relevance. List size is limited to n elements, and page 
        returns the given page of results */
    list<Artist> searchArtist (1: required string text, 2: required i32 n, 3: 
required i32 page) throws (1: TransientError t, 2: AuthenticationError a, 3: 
DataError d, 4: ProgrammingError p, 5: ServiceError s),
    
    /** Returns a list of the n top SE artists by decreasing value. Trange is 
        the number of days the leaderboard is over */
    list<ArtistSE> getSETop (1: required i32 n, 2: required i32 trange) throws 
(1: TransientError t, 2: AuthenticationError a, 3: DataError d, 4: 
ProgrammingError p, 5: ServiceError s),
    
    /** Returns a list of the n top last.fm artists by decreasing value. */
    list<ArtistSE> getLFMTop (1: required i32 n) throws (1: TransientError t, 
2: AuthenticationError a, 3: DataError d, 4: ProgrammingError p, 5: 
ServiceError s),
    
    /** Returns a list of the n most traded artists by decreasing value. */
    list<ArtistSE> getTradedArtists (1: required i32 n) throws (1: 
TransientError t, 2: AuthenticationError a, 3: DataError d, 4: ProgrammingError 
p, 5: ServiceError s),
    
    /** Returns a list of the n most recent trades */
    list<ArtistSE> getRecentTrades (1: required i32 n) throws (1: 
TransientError t, 2: AuthenticationError a, 3: DataError d, 4: ProgrammingError 
p, 5: ServiceError s),
    
    # User
   
    /** Returns extended user data for the current user. */
    UserData getUserData (1: required string user) throws (1: DataError d),
    
    /** Returns the current user with money. Requires AuthUser to auth */
    AuthUser getUserMoney (1: required AuthUser user) throws (1: DataError d),
    
    /** Returns the n top users by decreasing value in the given league. Trange 
        is the number of days the leaderboard is over, rounded to the nearest 
        day, week or month. */
    UserLeaderboard getTopUsers (1: required i32 n, 2: required League league, 
3: required i32 trange) throws (1: DataError d),
    
    /** Returns a list of 10 users with 4 above and 5 below in the leaderboard 
        compared to the user provided, including the user's position. */
    UserLeaderboard getNearUsers (1: required string user) throws (1: 
DataError d),
    
    # Data Modification
    
    /** Returns the guarantee token (elephant) to the front end */
    Guarantee getGuarantee (1: required Artist artist, 2: required AuthUser 
user) throws (1: DataError d, 2: TransientError t),
    
    /** Buys artist for user, and returns a bool as to whether it was 
        successful or not */
    bool buy (1: required Guarantee guarantee, 2: required AuthUser 
user) throws (1: DataError d, 2: TransientError t),
    
    /** Sells artist for user, and returns a bool as to whether it was 
        successful or not */
    bool sell (1: required Guarantee guarantee, 2: required AuthUser 
user) throws (1: DataError d, 2: TransientError t)
   
}
