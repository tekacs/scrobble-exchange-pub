# Scrobble Exchange :: Analytics Backend

This is the branch containing the Scrobble Exchange analytics backend.

Structure:

- vendor/ :: for imported libraries
- lib/ :: application logic
- analytics.py :: server launch/... code ('entry point')

Requirements:

+ Must be the single source for daily data fetched and then cached from last.fm
    + Even if metrics are not calculated on data, if it is on the daily cycle, it should be fetched herein.
+ Must calculate all metrics about last.fm-sourced data.
    (to be combined with user-side data for actual use)
+ Must be designed to run only for as long as is required to perform its duties.
    + Such that it might be scheduled to run once daily.
    + This may be used, for example, to lock trading by the API for the duration of the day's data fetch.

Guarantees:

+ Will be the single source for last.fm data in the backend database
    (stored last.fm-sourced data shall *never* be modified in place by any other part of the application)
+ DATM and pyLast will provide any calls required to access last.fm or the database

Potential pitfalls:

+ Concurrency need likely be introduced in order to make bulk usage of API calls performant. - [AS][]
+ This program should be very carefully guarded against crashes during its operation. - [AS][]
    + The API will likely be locked during its operation as an anti-cheating measure.
    + Whilst it would be possible to recover from a crashed process, large portions of the database would need to be flushed and then re-fetched in order to guarantee consistent state.
    + Crashing mid-way would nullify the benefit of the first of the guarantees above - the database should be left in a consistent state upon every exit!
    + If there is any risk of crashes: - [AS][]
        + Use transactions to group changesets.
            This would require DATM support!
        + Use a journal/logging to ensure that the currently committed state can be determined.

Current assigned:

* Karolis Dziedzelis
* Amar Sood

<a id="amar">AS: Posited by Amar on a technical basis - poke me if you have objections/problems.</a>

[AS]: #amar "Posited by Amar on a technical basis - poke me if you have objections/problems."