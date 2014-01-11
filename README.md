# Scrobble Exchange: A massively multiplayer game

Branches:
* [master](https://github.com/tekacs/scrobble-exchange-pub)
* [doc](https://github.com/tekacs/scrobble-exchange-pub/tree/doc)
* [web](https://github.com/tekacs/scrobble-exchange-pub/tree/web) [chiefly Joe, Neil]
* [api](https://github.com/tekacs/scrobble-exchange-pub/tree/api) [chiefly Victor]
* [analytics](https://github.com/tekacs/scrobble-exchange-pub/tree/analytics) [chiefly Amar]
* [datm](https://github.com/tekacs/scrobble-exchange-pub/tree/datm) [chiefly Amar]

There is currently supposed to be nothing in this branch but for the README and branches.sh.

Please don't commit files in here!

Please also be very wary of `git pull origin <branch>` - it *will* merge all changes pulled into the current branch.
If you accidentally do this, please nuke your local repo and re-`clone`, unpick the merge carefully, or _ask_ if unsure.

The simplest solution is to just use branches.sh and work with the branches in different folders so that `git push/pull` will do everything for you.<sup>[1][]</sup>

Files:
* branches.sh :: This checks out all of the branches for you and sets them up such that you can push and pull changes to the right place with just a 'git push/pull' (i.e. without 'origin <...>')

Useful Links:
* Might I heartily recommend [Github for Mac](http://mac.github.com) and [GitHub for Windows](http://windows.github.com) to those unfamiliar with Git?

Team Members:[2][]

* Amar Sood (Lead Dev, Lead DATM)
* Neil Satra
* Victor Mikhno (Lead API)
* Guoqiang Liang
* Karolis Dziedzelis (Lead Analytics)
* Joe Bateson (Lead Frontend)

(reverse surname order, clearly :P)

<a id="footnote1">1.</a> If you really must use multiple branches in one tree, please remember that the correct command to grab a branch without merging changes is `git fetch origin <branch>`.
<a id="footnote2">2.</a> (hint: read 'Lead' as 'person to blame/ask about said tree' or 'person responsible for making sure it actually happens')
[1]: #footnote1
[2]: #footnote2
