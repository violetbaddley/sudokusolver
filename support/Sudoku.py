"""
The module which understands the variables at play in Sudoku,
and runs a backtracking-with-forward-checking-based algorithm to solve a board,
with "sprinkles": mrv, forward checking, and arc consistency, if opted.

Talus Baddley
October 2012
"""


import Board
import sys
import bookkeeping



# Use varying modules based on arguments.
# Much null pattern at work here.

if "-mrv" in sys.argv:
    import MRVChooser as mrv
else:
    import ArbitraryChooser as mrv


if "-lcv" in sys.argv:
    import LCVChooser as lcv
else:
    import ArbitraryChooser as lcv



import ForwardChecker as fwdcheck

if "-ac3" in sys.argv:
    import ArcChecker as ac3
else:
    import NoChecker as ac3


runStats = ("-stats" in sys.argv)
doProg = ("-noprog" not in sys.argv) and ("-tonly" not in sys.argv)








def solve(gameBoard):
    """ Run the sudoku solving algorithm on the given Board. """
    
    if gameBoard.isFull(): return gameBoard
    
    chosenSquare = mrv.ordering(gameBoard)
    for someValue in lcv.ordering(gameBoard, chosenSquare):
        
        # Place the provisional value on a test board.
        testBoard = gameBoard.copy()
        testBoard.placeValueAt(someValue, chosenSquare)
        
        # Winnow domains by forward checking:
        fwdcheck.checkBoard(testBoard, chosenSquare)
        if not testBoard.areAllDomainsOpen(): continue
        if runStats: bookkeeping.boardsPassedFwdcheck += 1
        
        # Winnow domains further by AC3:
        ac3.checkBoard(testBoard)
        if not testBoard.areAllDomainsOpen(): continue
        if runStats: bookkeeping.boardsPassedAc3 += 1
        
        # Provisional value OK,
        # punt down and try next square.
        if doProg: bookkeeping.reportPunt()
        puntBoard = solve(testBoard)    # <--------- Recursive Call
        if doProg: bookkeeping.reportShoonk()
        if puntBoard is not None: return puntBoard
        
        
    if runStats: bookkeeping.impossibleBoards += 1
    return None  # Implicitly no solution
    
