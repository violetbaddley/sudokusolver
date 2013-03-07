sudokusolver
============

A modular sudoku-solving program, in Python.



Running
-------

The main file to run is `sudokusolver.py`. Alternatively, you can use `SudokUI`, a Cocoa wrapper around the same script.

By default, `sudokusolver.py` runs using forward-checking only. If you want more brains, specify any combination of the following options when calling it:

    -mrv
    -lcv
    -ac3

which map to the features of the same name. I also highly recommend just calling

    ./sudokusolver.py

to see a listing of all the options that are available, including keeping track of various statistics.



What Makes it Go
----------------

The main script is really just a front; the real brains are found in the support folder. All those modules (plus the Board class) have descriptive comments, but in “Layout.pdf” is a graphical overview of how they all fit together.



The Cocoa Wrapper
-----------------


The `/SudokUI` project can be built in recent versions of Xcode. **However!** You must run sudokusolver once and copy the resulting `.pyc` files into the `/SudokUI/SudokUI` subfolder—the xcodeproj will be looking for them there.
