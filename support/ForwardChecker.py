'''
Checks a sudoku board and updates its domains accordingly

Talus Baddley
October 2012
'''

import bookkeeping

def checkBoard(sudBoard, square):
    '''
    Winnow the board's domains based on a placement in `square`,
    assuming the value has already been placed there.
    '''
    row, col = square
    newValue = sudBoard.values[row][col]
    domainers = bookkeeping.affectedSquaresFor(square)
    for modSquare in domainers:
        row, col = modSquare
        sudBoard.domains[row][col].discard(newValue)

