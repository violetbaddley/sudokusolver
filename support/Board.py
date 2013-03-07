"""
A Sudoku Board Object.

Direct access is provided to the underlying 9x9 grids:
`values` contains the numbers actually placed on the board (1-9 or None);
`domains`, at each square, contains the Set of numbers that can be placed there.

For simplicity of the algorithm (and, perhaps, in detriment of efficiency),
the Sudoku module duplicates the entire board at each placement.

Note that, throughout this project, the term "square" often refers to
a (row, column) tuple used to *locate* an actual square on the sudoku board.

Talus Baddley
October 2012.

"""

from copy import deepcopy
import ForwardChecker as fwdcheck


class Board:
    boardsCreated = 0  # for statistical purposes

    def __init__(self, numberList, *extras):
        """
        The specified `numberList` is deep-copied and used
        as the initial value state of the board.
        
        The second parameter is reserved for internal use.
        
        """
        Board.boardsCreated += 1
        self.values = deepcopy(numberList)
        if len(extras) == 1:
            # The actual domains have been handed down;
            # no calculatin' necessary. We're done.
            self.domains = deepcopy(extras[0])
            return
        
        # Under normal circumstances, calculate the domains:
        self.domains = []
        if len(self.values) != 9: raise ValueError('Incorrect Board Height')
        
        # Make the initial domains---either 1..9 or the empty set.
        for valueRow in self.values:
            if len(valueRow) != 9: raise ValueError('Incorrect Board Width')
            rowAdd = []
            for value in valueRow:
                if value is None:
                    rowAdd.append(set(range(1,10)))
                elif value < 1 or value > 9:
                    raise ValueError('Invalid Sudoku Number')
                else:
                    rowAdd.append(set([]))  # THE EMPTY SET

            self.domains.append(rowAdd)
        
        # Now perform 0th 'forward checking'.
        self.winnowDomainsByExistingValues()

    
    def copy(self):
        # A copy is just a construction where the domain needn't be recalculated.
        return Board(self.values, self.domains)

    def winnowDomainsByExistingValues(self):
        """
        Used to establish existing domains
        when a brand new (uncopied) board is created.
        """
        for someSquare in [(row, col) for row in range(9) for col in range(9)
                           if (self.values[row][col] is not None)]:
            fwdcheck.checkBoard(self, someSquare)
    
    
    def placeValueAt(self, value, at):
        """
        Place `value` onto the board (valid or not) at the square called `at`
        and clear that position's domain.
        """
        row, col = at
        self.values[row][col] = value
        self.domains[row][col] = set([])

        
    def isValidValueAt(self, value, at):
        """
        Check whether `value` would be a valid placement on the board
        at the square called `at`.
        """
        # Does anyone ever actually call this method?
        row, col = at
        return (value in self.domains[row][col])

    
    def isFull(self):
        """ Checks whether the board is full (done). """
        for row in self.values:
            for value in row:
                if value is None: return False
        return True

    
    def areAllDomainsOpen(self):
        """
        Checks whether all the board's domains are "open";
        that is, whether all blank squares have a non-empty domain.
        """
        for valueRow, domainRow in zip(self.values, self.domains):
            for value, domain in zip(valueRow, domainRow):
                if value is None and len(domain) == 0: return False
        return True

    def openSquares(self):
        """
        Returns a list of all squares which are not filled,
        (not necessarily those with open domains).
        """
        return [(row, col) for row in range(9) for col in range(9)
                if self.values[row][col] is None]



    
    def __str__(self):
        processedLines = [' '.join([ ( '*' if value is None else str(value) )
                                     for value in row ])
                          for row in self.values]
        return '\n'.join( processedLines )
