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

/** Basic artist info. Imageurl is a mapping to the image url from its 
respective size */
struct Artist {
    1: optional string name
    2: required string mbid
    3: optional string url
    4: optional map<string,string> imageurl
}

/** Keeps a list of artist values in time
    Ordered list by date from oldest to newest
    Format is <date,value>, both integers
    Timeonmarket might help in drawing the graphs (Unsure?) */
struct ArtistHistory {
    1: required list<map<i32,i32>> histvalues
    2: optional i32 timeonmarket
}

/** Contains all the data about the artist we have in our db
    For a new artist, stockvalue = curmarketvalue, and ArtistHistory would just 
    have an empty list. curforsale is the current amount available to be 
    bought */ 
struct ArtistSE {
    1: required Artist artist
    2: required i32 stockvalue
    3: required i32 curmarketprice
    4: required i32 curforsale
    5: optional ArtistHistory history
}

/** Essentially encapsulates the data from last.fm's artist.getInfo. It's 
    entirely possible that this won't be needed. */
struct ArtistLFM {
    1: required Artist artist
    2: required bool streamable
    3: required i32 listeners
    4: required i32 plays
    5: optional list<Artist> similar
    6: required string bio
}

# User

/** User has some stuff on the market. Time is the amount of time you've been 
    trying to buy/sell this stock */
struct Trade {
    1: required Artist artist
    2: required i32 price
    3: optional i32 time
}

/** User trophies. Desc is an extended description, and challenge is a possible 
    arbitrary `difficulty to obtain' measurement */
struct Trophy {
    1: required string name
    2: required string description
    3: optional string challenge
}

/** Basic user info. This is all that is needed for most pages where the user 
    isn't the primary content. */
struct User {
    1: required string name
    2: required i32 money
}

/** Encapsulates all the user data. For a new user, curtrades and curstocks 
    will be empty lists. Since we're unsure of how leaderboards will work, that 
    part of the user data is currently probably in an odd format */
struct UserData {
    1: required User user
    2: required list<Trade> curtrades
    3: required list<ArtistSE> curstocks
    4: required list<Trophy> curtrophies
    5: optional i32 leaderboardpos
}

/** Encapsulates all the user info for profile pages */
struct UserInfo {
    1: required User user
    2: optional list<Trade> rectrades
}

# Transaction

/** Encapsulates the guarantee for purchase that is provided to the user. */
struct Transaction {
    1: required string elephant
    2: required i32 value
    3: required i32 time
}

## Exceptions
# These really need to be filled out with all of the actual errors that could 
# occur.

exception AccountException {
}

exception AuthException {
    1: required string why
}

exception SearchException {
    1: required string why
}

exception TransactionException {
    1: required string why
}

exception UserException {
    1: required string why
}

## Service definition

service ScrobbleExchange {
   
    # Login
    
    /** If successful, returns the user token. If not, returns an 
        AuthException. AccountException is returned if account data is 
        incorrect or doesn't exist, and should be handled appropriately */
    string login(1: required string token) throws (1: AuthException authexp, 2: 
AccountException accexp),
    
    # Data retrieval
    # Artists
    
    /** Returns basic artist info. Artist string can be either the name, or the 
        musicbrainz ID */
    Artist getArtist (1: required Artist artist) throws (1: SearchException 
searchexp),
    
    /** Returns the data from our db for the artist. 
        Assumes that if artist isn't in the DB, then it gets pulled in 
        on-demand and so will always return some data.
        Artist string can be either the name, or the musicbrainz ID */
    ArtistSE getArtistSE (1: required Artist artist) throws 
(1: SearchException searchexp),
    
    /** Returns the contextual artist info from last.fm for the artist
        Artist string can be either the name or the musicbrainz ID */
    ArtistLFM getArtistLFM (1: required Artist artist) throws (1: 
SearchException searchexp),
    
    /** returns a list of possible artists from a partial string. Ordered by 
        decreasing relevance. List size is limited to 5 elements. */
    list<Artist> searchArtist (1: required string text) throws (1: 
SearchException searchexp),
    
    /** Returns a list of the n top artists by decreasing value. By default, tag
        should have a value of '' and only be used if you want to limit the 
        top lists to a certain tag. */
    list<Artist> getTopArtists (1: required i32 n, 2: string tag),
    
    /** Returns a list of the n most traded artists by decreasing value. */
    list<Artist> getTradedArtists (1: required i32 n), 
    
    # User
   
    /** Returns extended user data for the current user */
    UserData getUserData (1: required User user) throws (1: UserException 
uexp),
    
    /** Returns extended user data for the user in the string. Mostly, used for 
        profile pages */
    UserInfo getUserInfo (1: required string user) throws (1: UserException 
uexp),
    
    /** Returns the n top users by decreasing value in the given league. */
    list<User> getTopUsers (1: required i32 n, 2: required string league) 
throws (1: UserException uexp),
    
    /** Returns a list of 10 users with 4 above and 5 below in the leaderboard 
        compared to the user provided */
    list<User> getNearUsers (1: required string user) throws (1: UserException 
uexp),
    
    # Data Modification
    
    /** Returns the guarantee token to the front end */
    Transaction getTransaction (1: required Artist artist) throws (1: 
TransactionException transexp),
    
    /** Buys artist for user, and returns the new value of that stock in the 
        game. Throws a transaction exception if something goes wrong while 
        buying or the user can't afford to buy the artist.
        Throws user exception if the user already owns the stock */
    i32 buyArtist (1: required Transaction transaction, 2: required User user) 
throws (1: TransactionException transexp, 2: UserException userexp),
    
    /** Sells artist for user, and returns the new value of that artist. User 
        exception is thrown if the user isn't allowed to sell or doesn't own 
        that artist */
    i32 sellArtist (1: required Transaction transaction, 2: required User user) 
throws (1: TransactionException transexp, 2: UserException userexp)
   
}
