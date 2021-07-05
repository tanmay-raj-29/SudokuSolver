import fileinput
import time

def print_sudoku(board):
    """
    Format the Sudoku (currently in a 2D list) into
    a grid with lines separating the blocks to improve readability
    """
    output = ""
    for row in range(9):
        for col in range(9):
            output += (str(board[row][col]) + " ")
            if col+1 == 3 or col+1 == 6:
                output += (" | ")
        if row+1 == 3 or row+1 == 6:
            output += ("\n" + "-"*25)
        output += '\n'
    output += '\n'

    print(output)

def test_cell(board, row, col):
    """
    For a given cell, returns the the possibility of each digit to go in that cell
    0 = not possible, 1 = possible
    """
    used = [1]*10
    used[0] = 0
    row_block = row // 3
    col_block = col // 3

    # Row and Column
    for m in range(9):
        used[board[m][col]] = 0;
        used[board[row][m]] = 0;

    # Square
    for m in range(3):
        for n in range(3):
            used[board[m + row_block*3][n + col_block*3]] = 0

    return used

def initial_try(board):
    """
    For a Sudoku puzzle, tries to solve the puzzle by iterating through each
    cell and checking the possible candidates for that cell. If only one possible
    candidate exists, fill it in and continue on until the puzzle is stuck.
    """
    stuck = False

    while not stuck:
        stuck = True
        # Iterate through the Sudoku puzzle
        for row in range(9):
            for col in range(9):
                used = test_cell(board, row, col)
                # More than one possibility
                if used.count(1) != 1:
                    continue

                for m in range(1, 10):
                    if board[row][col] == 0 and used[m] == 1:
                        # current cell is empty and digit m is possible
                        board[row][col] = m
                        stuck = False
                        break

def DFS_solve(board, row, col):
    """
    For a Sudoku puzzle, solve the puzzle by recursively performing DFS
    which tries out all the possible solutions and backtracking to eliminate 
    the invalid tries and all the possible cases arising from those tries
    """
    if row == 8 and col == 8:
        used = test_cell(board, row, col)
        if 1 in used:
            board[row][col] = used.index(1)
        return True

    if col == 9:
        row = row+1
        col = 0

    if board[row][col] == 0:
        used = test_cell(board, row, col)
        for i in range(1, 10):
            if used[i] == 1:
                board[row][col] = i
                if DFS_solve(board, row, col+1):
                    return True

        # Reached here? Then we tried 1-9 without success
        board[row][col] = 0
        return False

    return DFS_solve(board, row, col+1)

def main():
    start = time.time()
    num_puzzles = 0
    board = []
    text = ""

    for line in fileinput.input():
        line = ' '.join(line.split())
        text += line

    while len(text) > 0:
        l = []

        # Get a row of numbers
        while len(l) < 9:
            if text[0].isdigit():
                l.append(int(text[0]))
            text = text[1:]

        # Insert that row into the Sudoku grid
        board.append(l)

        if len(board) == 9:
            num_puzzles += 1
            print("Puzzle Number {:d}".format(num_puzzles))
            print("Original:")
            print_sudoku(board)

            initial_try(board)
            for line in board:
                if 0 in line:
                    DFS_solve(board, 0, 0)
                    break

            print("Solution:")
            print_sudoku(board)

            print("="*30)
            board = []

    print("{:.2f} seconds to solve {} puzzles".format(time.time() - start, num_puzzles))
if __name__ == "__main__":
    main()