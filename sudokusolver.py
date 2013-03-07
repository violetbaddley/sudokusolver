#!/usr/bin/env python
# That means, "yes, run THIS file," specifically with encoding: utf-8

u"""
A program to solve a sudoku puzzle.

This is the main runnerfile.
It is very **strongly recommended** that you read over the usage
description (which you can get by running this program with no
puzzle provided) first.

The actual game logic is headed up in the Sudoku module.

Solver by Talus Baddley,
Copyright © 2012 Eightt Software.

"""


import sys, os, gc
import site
site.addsitedir('support')

import bookkeeping, Sudoku, BoardInterpreter



# Read in the file right up front
boardFile = bookkeeping.contentsOfFileSpecifiedIn(sys.argv[1:])


if boardFile is None:
    usageString = """
Usage: sudokusolver.py [board.txt] [-options]
    Either "board.txt" or standard-in should contain a valid sudoku board.
    You can also optionally specify any of the following options:
      -ac3     ---  check arc consistency
      -mrv     ---  select squares by min. remaining val.
      -lcv     ---  select values by least constraining
      -stats   ---  report the number of bad placements and backtracks
        -time  ---  always show time-to-solve in -stats
      -noprog  ---  process without der blinkenlights
      -po      ---  print out original board
      -nops    ---  don't print out solution (good with -stats)
"""
    
    print usageString
    sys.exit(0)


if '-gc-debug' in sys.argv:
	gc.set_debug(gc.DEBUG_STATS)

shouldPo = ('-po' in sys.argv)
shouldPs = not ('-nops' in sys.argv)
runStats = ('-stats' in sys.argv)


# Heavily undocumented hack:
if '-tonly' in sys.argv:
    timeOnly = True
    shouldPs = False
else:
    timeOnly = False




# Interpret a board object from the file data
gameBoard = BoardInterpreter.boardFromFile(boardFile)

if shouldPo:
    print 'Solving:'
    print gameBoard
    print ' '

if not timeOnly: bookkeeping.setupStatusLine()
bookkeeping.algorithmStarted()


# Ready,
# set.....
# GO!
solution = Sudoku.solve(gameBoard)

# whew!
timeToSolve = bookkeeping.algorithmEnded()
if not timeOnly: bookkeeping.teardownStatusLine()
if shouldPs:
    print 'Solution:'
    print (solution if solution is not None else 'No solution.')
    print ' '


if runStats:
    print '    Steps (Boards Surmised):', bookkeeping.boardsCreated()
    print '     Bad Boards Backtracked:', bookkeeping.impossibleBoards
    print ' Boards Pruned (Fwd. Check):', bookkeeping.caughtByFwdcheck()
    print "Boards Pruned (Arc Const'y):", bookkeeping.caughtByAc3()
    if timeToSolve > 1 or ('-time' in sys.argv):
        print '              Time to Solve:', timeToSolve, 'nanodays'
        
if timeOnly:
    print timeToSolve
    

