import pySudoku
import sudokuChecker
import random
import time

def toString(board, to_format = False):
    """
    Formats a 2D list Sudoku puzzle into a 9x9 grid or 
    one line of integers depending on the to_format varibale.
    By default if formats it to a line fo integers
    """    
    output = ""
    if to_format:
        for row in range(9):
            for col in range(9):
                output += (str(board[row][col]) + " ")
                if col+1 == 3 or col+1 == 6:
                    output += (" | ")
            if row+1 == 3 or row+1 == 6:
                output += ("\n" + "-"*25)
            output += '\n'
        output += '\n'
    else:
        for i in range(9):
            for j in range(9):
                output += str(board[i][j])
    return output + "\n"

def populateBoard(board, row, col):
    """
    Given a 9x9 grid of 0's, it recursively fills
    the grid. Makes a list of integers from 1-9, shuffles the list, and
    checks for the first integer in the list which can be inserted at the cell.
    If found it inserts it in the current cell and continues on.
    If none of the integers work, then it returns false.
    """
    if row == 8 and col == 8:
        used = pySudoku.test_cell(board, row, col)
        board[row][col] = used.index(1)
        return True

    if col == 9:
        row = row+1
        col = 0

    temp = list(range(1, 10))
    random.shuffle(temp)
    # Fill Sudoku
    for i in range(9):
        board[row][col] = temp[i]
        if sudokuChecker.checkValid(board, row, col):
            if populateBoard(board, row, col+1):
                return True
    board[row][col] = 0
    return False

def DFS_solve(board_copy, row, col):
    """
    Recursively solves the board_copy puzzle with a DFS algorithm, 
    and returns the number of solutions found.
    Starts at row 0 and column 0
    """
    num_solutions = 0

    # Reached the last cell, so solution exits
    if row == 8 and col == 8:
        return num_solutions + 1

    if col == 9:
        row = row+1
        col = 0

    if board_copy[row][col] == 0:
        # Used = list of size 10 containing 0 and 1
        # 0 represents that the given index is not possible
        # 1 represents that the given index is possible.
        # Ignore index 0.
        used = pySudoku.test_cell(board_copy, row, col)
        # No possible solutions. Return 0 for number of solutions
        if 1 not in used:
            return 0

        while 1 in used:
            board_copy[row][col] = used.index(1)
            used[used.index(1)] = 0
            num_solutions += DFS_solve(board_copy, row, col+1)

        # Reached here? Then we tried 1-9 without success
        board_copy[row][col] = 0
        return num_solutions

    num_solutions += DFS_solve(board_copy, row, col+1)
    return num_solutions

def reduce_sudoku(board, difficulty):
    """
    Generates a list of integers 0-80 representing the indices
    of the puzzle and shuffles the order. Given a complete Sudoku puzzle
    (generated from populate_board fuction) tries to remove the number at 
    the first index in the list and then tries to solve it. 
    If there exist multiple solution, then it is not a valid
    Sudoku puzzle, so undo the last change. If easy puzzles are desired, then
    after a puzzle with a unique solution is found, algorithm stops. If difficult
    puzzles are wanted, then even after a valid puzzle is found, all the remaining
    indices are tried to see if the puzzle can be made any harder.
    """
    indices = list(range(81))
    random.shuffle(indices)

    while indices:
        row = indices[0] // 9
        col = indices[0] % 9
        temp = board[row][col]
        board[row][col] = 0
        indices = indices[1:]

        board_copy = [l[:] for l in board]

        pySudoku.initial_try(board_copy)

        for line in board_copy:
            if 0 in line:
                num_solutions = DFS_solve(board_copy, 0, 0)
                # No unique solution, so undo the last insertion
                if num_solutions > 1:
                    board[row][col] = temp
                    # If we want easy puzzles, we stop here after finding
                    # the first puzzle with a unique solution
                    # For harder puzzles we try to removing other elements and check
                    # if there is another puzzle with a unique solution
                    if difficulty == "E":
                        return
                break

    return

def main():
    f = open("SudokuPuzzles.txt", "w")
    user_input = int(input("How many Sudoku puzzles would you like to generate?:\n"))
    difficulty = 'A'
    while difficulty != 'E' and difficulty != 'D':
        difficulty = input("Do you want Easy or Difficult puzzles?: (E or D)\n")
    to_format = 'A'
    while to_format != 'Y' and to_format != 'N':
        to_format = input("Do you want puzzles to be formatted : (Y or N)\n") 
    if to_format == 'Y':
        to_format = True
    else:
        to_format = False
        
    start = time.time()

    for _ in range(user_input):
        # 9 x 9 grid of 0s
        board = [[0]*9 for _ in range(9)]

        populateBoard(board, 0, 0)
        reduce_sudoku(board, difficulty)
        output = toString(board, to_format)
        f.write(output)
        
    print("{:.2f} seconds to generate {} Sudoku puzzles.".format(time.time() - start, user_input))

if __name__ == '__main__':
    main()