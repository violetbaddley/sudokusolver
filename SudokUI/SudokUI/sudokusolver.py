#!/usr/bin/env python

import sys
import os

import bookkeeping
import BoardInterpreter
import Sudoku
import gc



''' Solve a Sudoku Board.
    This is the general driver file that starts up the game;
    the actual game logic is in Sudoku.py. '''


# Read in the file right up front
boardFile = bookkeeping.contentsOfFileSpecifiedIn(sys.argv)


if boardFile is None:
    usageString = """Usage: sudokusolver.py board.txt
    where "board.txt" contains a valid sudoku board.
    You can also optionally specify any of the following options:
      -ac3     ---  check arc consistency
      -mrv     ---  select squares by min. remaining val.
      -lcv     ---  select values by least constraining
      -stats   ---  report the number of bad placements and backtracks
        -time  ---  always show time-to-solve in -stats
      -noprog  ---  process without das blinkenlichten
      -po      ---  print out original board
      -nops    ---  don't print out solution (good with -stats)"""
    
    print usageString
    sys.exit(0)


if '-gc-debug' in sys.argv:
	gc.set_debug(gc.DEBUG_STATS)

shouldPo = ('-po' in sys.argv)
shouldPs = not ('-nops' in sys.argv)
runStats = ('-stats' in sys.argv)


gameBoard = BoardInterpreter.boardFromFile(boardFile)

if shouldPo:
    print 'Solving:'
    print gameBoard
    print ' '

bookkeeping.setupStatusLine()
bookkeeping.algorithmStarted()

solution = Sudoku.solve(gameBoard)

timeToSolve = bookkeeping.algorithmEnded()
bookkeeping.teardownStatusLine()
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
    

