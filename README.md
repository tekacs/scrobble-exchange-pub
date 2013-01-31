# Scrobble Exchange: A massively multiplayer game

## Group Project Charlie

There is currently supposed to be nothing in this branch but for the README and branches.sh.

Please don't commit files in here!

Please also be very wary of `git pull origin <branch>` - it *will* merge all changes pulled into the current branch.
If you accidentally do this, please nuke your local repo and re-`clone`, unpick the merge carefully, or _ask_ if unsure.

The simplest solution is to just use branches.sh and work with the branches in different folders so that `git push/pull` will do everything for you.<sup>[1][]</sup>

Files:
* branches.sh :: This checks out all of the branches for you and sets them up such that you can push and pull changes to the right place with just a 'git push/pull' (i.e. without 'origin <...>')

Resources:
* [Google Docs](https://docs.google.com/folder/d/0Bzc0w3Y7EvMeblByNnZ1Y1RieHc/edit) (for notes, documentation, etc.)
* [Facebook](https://www.facebook.com/groups/scrobble-exchange) (for conversation)
* [GitHub](http://github.com/tekacs/scrobble-exchange) (in case you're looking at the checked out repository)
* [IRC](irc://last.fm:6667/last.gp)

Useful Links:
* Might I heartily recommend [Github for Mac](http://mac.github.com) and [GitHub for Windows](http://windows.github.com) to those unfamiliar with Git?

Team Members:

* Amar Sood (Lead Dev)
* Neil Satra
* Victor Mikhno
* Guoqiang Liang
* Karolis Dziedzelis
* Joe Bateson (Lead Frontend)

(reverse surname order, clearly :P)

<a id="1">If you really must use multiple branches in one tree, please remember that the correct command to grab a branch without merging changes is `git fetch origin <branch>`.</a>
[1]: #1