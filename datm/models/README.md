# Comments about the files in this folder in general!

* Beware circular imports if trying to further split files!
* Please don't try to remove seemingly 'redundant' imports without a fair amount of thought!
    * If imports seem unnecessary, consider the effect of importing a given file in isolation.
    * Imports may work perfectly well when performed with the package structure intact (due to the magic of `__init__.py`) but would break down if individual files were extracted if not for the seemingly redundant imports.
* Please accept my apologies about the commented-out lines in several files.
    * The 'many-to-many' comments are a result of SQLAlchemy's backreferences for such relationships being defined only on one of the two classes involved.
    * There are some places where, as of the time of writing, an alternate schema possibility is commented out. This is to indicate a rejected choice which may be reinstated (with considerable thought) should the current solution prove insufficiently efficient.