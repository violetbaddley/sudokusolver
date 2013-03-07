"""
Creates Board objects from text-file sudoku boards.

Talus Baddley
October 2012.
"""

import string
from Board import Board

def boardFromFile(readFile):
    """
    Assume `readFile` is a line-iterable (list of strings, or
    a File object, etc.) and construct a sudoku Board.
    
    Squares are delimited by whitespace; blank lines are ignored.
    """
    
    matrix = []
    for boardLine in readFile:
        matrix.append([])
        for value in boardLine.rstrip().lstrip().split():
            matrix[-1].append( int(value)  if value in string.digits  else None )

        if len(matrix[-1]) == 0:
            matrix.pop()  # Non-board line. Remove.
    
    return Board(matrix)
