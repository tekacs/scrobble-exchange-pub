# Scrobble Exchange :: API

This is the branch containing the Scrobble Exchange private/public API client and server.

Structure:

- spec/ :: for autogeneration sources
- client/ :: for client libraries
- server/ :: for the API server

Requirements:

+ Must be versioned to support feature freezing periodically (to stop old clients from breaking on update)
+ Must present a usable Python client library.    
    + The reference implementation of a consumer of the API client library is the Scrobble Exchange website.
    + The API shall thus be designed to support the website in any way that is required of it.
+ Must present a long-running Python API server.
+ Must be able to handle very high request frequency. Must be able to distribute requests.
+ Must fail gracefully under high load - [AS][]
    + (return 500 errors sure, but don't simply lock up on requests)
+ Must perform all data access (read/write) through DATM - [AS][]

Potential pitfalls:

+ May be started in an environment subject to forking limitations or threading limitations - [AS][]
    + Forking is the more likely limitation - [AS][]
+ Please note that Python's implementation of threading (in most implementations) does not take advantage of SMP - [AS][]
+ Must not break down on long-running DATM calls (starvation, etc.) - [AS][]
    (to some extent DATM's problem - will try to present a decent async interface)

Current assigned:

* Victor Mikhno
* Amar Sood

<a id="amar">AS: Posited by Amar on a technical basis - poke me if you have objections/problems.</a>

[AS]: #amar "Posited by Amar on a technical basis - poke me if you have objections/problems."