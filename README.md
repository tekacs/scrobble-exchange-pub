# Scrobble Exchange :: Data Access Transparency Module

This is the branch containing the Scrobble Exchange DATM, or 'Data Access Transparency Module'.

(yes, that was the most obvious name that came to mind - DAAM ('Abstraction Module') was too hard to say)

Structure:

- `datm/` :: This folder is the Python module - it's enclosed to avoid other files becoming part of the root namespace of the module.
- `datm/__init__.py` :: May be empty to start with - don't delete it!
- `datm/<...>.py` :: Each file created houses the relevant part of the module and is exposed if added to `__all__` in `__init__.py`.
- config.example.py :: An example of how to configure DATM for use.

Requirements:

+ Must specify (and is the canonical definition of the) data model for the backend database.
+ Must provide api, web and analytics with a consistent way to access the database and last.fm API.
+ Must implement logic as appropriate to transform database/ORM-specific and similar objects to avoid coupling between DATM consumers and its upstream.
+ Must be thread-safe!
    + Especially for use by API, analytics.
+ Must recognise that access may be conducted concurrently with clients on other machines (API/web/analytics).
    + last.fm data will likely be locked for API writes during analytics refresh (for anti-cheating reasons).
    + web should never read or write data directly to the backend database
    + As a result of the above two reasons, the chief danger is the API conflicting with itself.
+ Must provide user authentication cross-SE/LFM.
+ Must be operable without access to the database (for last.fm API access by database-blind clients (such as web))
+ Should provide an asynchronous way of making calls if sanely possible.
    + May use threads to accomplish this goal (Python doesn't use native threads after all) but should be wary.
    + Amar is tempted to use CP but wonders if that might be overkill. Control is henceforth returned to Amar, context intact.

Guarantees:

+ Will be the only library used by the rest of SE to interact with the database/LFM.
    + Caching may thus be done appropriately, for example.
    + It should be noted that all clients using this library will not necessarily be on the same machine - caching, etc. must be done on known remotes.
+ This library will not be handed out publicly.
    + This is _not_ an excuse for security-through-obscurity or 'hidden' debug calls.
    + This is _not_ a reason to hard-code credentials.
    + This _is_ a reason to allow coupling between database and LFM access as required - this is not meant for general LFM access or similar.

Potential pitfalls: In Amar's head for the moment, since he writes these sections and is too lazy to write them down for his own tree right now.

Dependencies:

- Postgres server :: backing database
- SQLAlchemy :: ORM
<!-- TBD
- MongoDB server :: backing document database
- PyMongo :: for accessing MongoDB
-->

Current assigned:

* Amar Sood (Lead Dev, Lead DATM)
* Karolis Dziedzelis
* Neil Satra

<a id="amar">AS:</a> Posited by Amar on a technical basis - poke me if you have objections/problems.

[AS]: #amar "Posited by Amar on a technical basis - poke me if you have objections/problems."