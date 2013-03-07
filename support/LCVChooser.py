"""
Orders domain values in a square
by least constraint of neighboring squares.

Talus Baddley
October 2012.
"""

import Board
import bookkeeping

def ordering(sudBoard, square):
    """ Select values for a given square in order of least constraining. """
    # Very much based on ArcChecker
    valueAllowanceList = []
    row, col = square
    for possibility in sudBoard.domains[row][col]:
        # Suppose possibility is chosen; how workable are the neighbors?
        allowance = _trySquare(sudBoard, square, possibility)
        valueAllowanceList.append((possibility, allowance))
            
    valueAllowanceList.sort( key = lambda va: va[1], reverse = True )
    #import pdb; pdb.set_trace()
    return map(lambda va: va[0], valueAllowanceList)


def _trySquare(sudBoard, square, value):
    """ Checks constrainingness for a value of a square on its neighbors """
    # `allowance` is the count of all remaining neighboring
    # domain values after setting `value` in `square`.
    allowance = 0
    for testDomain in [sudBoard.domains[row][col] for row, col
                       in bookkeeping.affectedSquaresFor(square)]:
        discardDomain = testDomain.copy()
        discardDomain.discard(value)
        allowance += len(discardDomain)

    return allowance
