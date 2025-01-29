import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import generate_sudoku
from generator import check_unique_solution

def test_valid_numbers():
    """ Test if all numbers in the generated sudoku are between 1 and 9 """
    sudoku = generate_sudoku()
    assert all(1 <= num <= 9 for row in sudoku for num in row)

def test_unique_in_rows():
    """ Test if all numbers in the rows are unique """
    sudoku = generate_sudoku()
    for row in sudoku:
        assert len(set(row)) == 9

def test_unique_in_columns():
    """ Test if all numbers in the columns are unique """
    sudoku = generate_sudoku()
    for col in range(9):
        column = [sudoku[row][col] for row in range(9)]
        assert len(set(column)) == 9

def test_unique_in_boxes():
    """ Test if all numbers in the 3x3 boxes are unique """
    sudoku = generate_sudoku()
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(sudoku[box_row + i][box_col + j])
    assert len(set(box)) == 9

def test_check_unique_solution_unique():
    """ Test if check_unique_solution correctly identifies unique solutions """
    grid = np.array([
        [1, 2, 0, 7, 8, 6, 9, 5, 4],
        [9, 4, 6, 2, 5, 1, 8, 3, 7],
        [8, 7, 5, 9, 4, 3, 6, 2, 1],
        [6, 3, 1, 8, 7, 5, 4, 9, 2],
        [4, 5, 8, 1, 2, 9, 3, 7, 6],
        [7, 9, 2, 6, 3, 4, 1, 8, 5],
        [2, 1, 9, 5, 6, 8, 7, 4, 3],
        [3, 6, 7, 4, 9, 2, 5, 1, 8],
        [5, 8, 4, 3, 1, 7, 2, 6, 9]
    ])
    last_pos = [0, 2]
    last_removed = 3
    assert check_unique_solution(grid, last_pos, last_removed) == True

def test_check_unique_solution_non_unique():
    """ Test if check_unique_solution correctly identifies non-unique solutions """
    grid = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    last_pos = [0, 2]
    last_removed = 2
    assert check_unique_solution(grid, last_pos, last_removed) == False