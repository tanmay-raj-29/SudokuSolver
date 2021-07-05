def checkValid(s, row, col):
    """
    Returns whether a given cell is valid in the Sudoku puzzl. 
    A cell is valid if the number in that cell is not present
    in any of the cells in the same row, or the same column, or the same block.
    """
    row_block = row // 3
    col_block = col // 3

    # Row and Column
    # Ignore blank spots
    for m in range(9):
        if s[row][m] != 0 and m != col and s[row][m] == s[row][col]:
            return False
        if s[m][col] != 0 and m != row and s[m][col] == s[row][col]:
            return False

    # Block
    for m in range(3):
        for n in range(3):
            newRow = m + row_block*3
            newCol = n + col_block*3
            if s[newRow][newCol] != 0 and newRow != row and newCol != col\
            and s[newRow][newCol ] == s[row][col]:
                return False

    return True

def checkSolution(board):
    for row in range(9):
        for col in range(9):
            if(checkValid(board, row, col) == False):
                return False
    return True