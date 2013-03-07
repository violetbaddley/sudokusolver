"""
Checks a sudoku board for arc consistency.

Talus Baddley
October 2012

"""

import Board
import bookkeeping

def checkBoard(sudBoard):
    """ Winnows the board's domains for arc consistency. """
    for square, domain in [ ((row, col), sudBoard.domains[row][col])
                            for (row, col) in sudBoard.openSquares() ]:
        for possibility in domain.copy():
            # Suppose possibility is chosen; is every other square workable?
            possibilityOK = _trySquare(sudBoard, square, possibility)
            if not possibilityOK:
                domain.discard(possibility)


def _trySquare(sudBoard, square, value):
    """
    Checks the consistency of a particular board placement
    against every other applicable board square.
    
    """
    for testDomain in [sudBoard.domains[row][col] for row, col
                       in bookkeeping.affectedSquaresFor(square)]:
        if len(testDomain) == 1:
            discardDomain = testDomain.copy()
            discardDomain.discard(value)
            if len(discardDomain) == 0: return False

    return True

