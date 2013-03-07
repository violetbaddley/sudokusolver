"""
Some bookkeeping & boilerplate stuff to keep the sudoku solver
running smoothly with fewer interspersed uglies.
Also mangles & manages the runtime stats.

Talus Baddley
October 2012.
"""


from Board import Board
from sys import stdout, stdin
import time

def contentsOfFileSpecifiedIn(argv):
    """
    Find the first file specified in the arguments,
	and return its contents, as a list of its lines.
	
    """
    for argument in argv:
        try:
            with open(argument) as testFile:
                return testFile.readlines()
        except EnvironmentError:
            pass  # Expect many to not be files.
        
    # No file specified, try stdin
    try:
        if not stdin.isatty():
            return stdin.readlines()  # Read, but only from non-interactive stdin
    except EnvironmentError:
       pass  # Give up.
    return None




# This section provides functions which enumerate
# the zones of the board affected by number placement
# in a particular square.


def boxFor(square):
    ''' Return all the other squares contained by the given square's box '''
    down, right = square
    top, bot, lef, rt = 0, 3, 0, 3
    if down > 2:
        top, bot = ((3, 6) if down < 6 else (6, 9))
    if right > 2:
        lef, rt = ((3, 6) if right < 6 else (6, 9))
    
    return [ (row, col) for row in range(top, bot) for col in range(lef, rt)
             if ( (row, col) != square ) ]
        
def colFor(square):
    ''' Return all the other squares in the given square's column '''
    vPos, hPos = square
    return [ (row, hPos) for row in range(9) if row != vPos ]

def rowFor(square):
    ''' Return all the other squares in the given square's row '''
    vPos, hPos = square
    return [ (vPos, col) for col in range(9) if col != hPos ]

def affectedSquaresFor(square):
    """ Return the set of all other squares that changing the argument might affect. """
    return set(boxFor(square)).union(colFor(square)).union(rowFor(square))





# This section for statistical purposes #
# Note that the Board class keeps track of its own creation count.
# The Sudoku module updates the other counts here.

impossibleBoards = 0
boardsPassedFwdcheck = 0
boardsPassedAc3 = 0
startTime = 0

def caughtByFwdcheck():
    return Board.boardsCreated - boardsPassedFwdcheck

def caughtByAc3():
    return boardsPassedFwdcheck - boardsPassedAc3

def boardsCreated():
    return Board.boardsCreated

def algorithmStarted():
    startTime = time.clock()

def algorithmEnded():
    return (time.clock() - startTime) / 0.864  # Nanodays -_^




# Print some Dots

def setupStatusLine():
    stdout.write('Working')

def reportPunt():
    stdout.write('.')
    stdout.flush()

def reportShoonk():
    # This says 'one space back, end-of-line kill.'
    stdout.write('\x1b[ 1 D\x1b[ 0 K')
    stdout.flush()

def teardownStatusLine():
    # This says 'back up to head-of-line, kill.'
    stdout.write('\r\x1b[ 2 K')  # 
