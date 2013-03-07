"""
A null lister of some values.

Can act in place of value-ordering selectors (like lcv)
or in place of square-choosing selectors (like mrv).

Talus Baddley
October 2012
"""

import Board

def ordering(sudBoard, *square):
    """
    Return an arbitrary [list of] value[s].
    
    If `square` is given, return all available values for that square,
    in some order, as in lcv.
    Otherwise, return any open square on the board, as in mrv.
    """
    
    if len(square) > 0:
        row, col = square[0]  # It's a tuple of a single tuple, you see.
        availSet = sudBoard.domains[row][col]
        return [item for item in availSet]
        
    else:
        for row in range(9):
            for col in range(9):
                if len( sudBoard.domains[row][col] ) != 0:
                    return (row, col)

