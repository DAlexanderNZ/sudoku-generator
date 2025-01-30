""" Python script to generate vaild sudoku puzzles. """

import random
import numpy as np

class SudokuGenerator:

    def is_valid(self, grid, num, pos, board_size=9):
        """ Check if the number is valid at the given position """
        # Check row
        for x in range(board_size):
            if grid[pos[0]][x] == num and pos[1] != x:
                return False
                
        # Check column
        for x in range(board_size):
            if grid[x][pos[1]] == num and pos[0] != x:
                return False
        
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def generate_sudoku(self, board_size=9):
        """ 
            Generate a valid sudoku puzzle.
            First we generate 3 3x3 grids with a set of 1 - 9 in random order.
            These are the diagonal elements of the final sudoku puzzle.
            We then fill the rest of the grid by backtracking.
            board_size: int - The size of the board, default is 9.
        """
        #TODO: Support for different board sizes.

        def solve_grid():
            """ Fill the rest of the grid by backtracking """
            for i in range(board_size):
                for j in range(board_size):
                    if grid[i][j] == 0:
                        for num in random.sample(range(1, 10), 9):
                            if self.is_valid(grid, num, [i, j]):
                                grid[i][j] = num
                                if solve_grid():
                                    return True
                                grid[i][j] = 0
                        return False
            return True
        
        # Create an empty 9x9 grid.
        grid = np.zeros((board_size, board_size), dtype=int)
        # Fill the diagonal elements with 3 3x3 grids.
        for p in range(3):
            # Create an empty 3x3 grid.
            grid3 = np.zeros((3, 3), dtype=int)
            # Fill the grid with 1 - 9 in random order.
            candidates = list(range(1, board_size + 1))
            random.shuffle(candidates)
            for i in range(3):
                for j in range(3):
                    grid3[i, j] = candidates[-1]
                    candidates.pop()
            # Add the 3x3 grid to the main grid at diagonal 3x3 positions.
            offset = p * 3
            for i in range(3):
                for j in range(3):
                    grid[i + offset, j + offset] = grid3[i, j]

        solve_grid()
        return grid

    def check_unique_solution(self, grid, last_pos,  last_removed):
        """ 
            Check if the removed number is part of a unique solution.
            Returns True if the puzzle has a unique solution, False otherwise.
        """
        for num in range(1, grid.shape[0] + 1):
            if num != last_removed and self.is_valid(grid, num, last_pos):
                return False
        return True

    def redact_sudoku(self, grid, difficulty=0.5):
        """ 
            Redact the sudoku puzzle by removing numbers. 
            Max difficulty has 17 numbers remaining, don't allow less than 17 numbers for 9x9 grid.
            difficulty: 0.0-.79, higher means more numbers removed, > 0.79 on a 9x9 grid results in less than 17 numbers left.
        """
        size = grid.shape[0]
        total_cells = size * size
        min_cells = 17
        # Calculate the minimum number of cells to redact
        cells_to_keep = max(min_cells, int(total_cells * (1 - difficulty)) - 1)
        """
        1. Select a random cell from the board. If the cell is not-empty and not-visited continue to step 2. If the cell is visited move to step 6.
        2. Remove the selected cell from the game board.
        3. Calculate solutions for the removed cell on the board. If the uniqueness is achieved in solutions, continue to step 4. If there are more than 1 solution to the given removed cell, undo the removal.
        4. Set the current cell as zero.
        5. Return to step 2.
        5. Repeat step 2 until random and cells_to_keep count is 0.
        """
        successfull_redactions = False
        attempts = 0
        best_attempt_redaction_count = 0
        best_attempt = grid.copy()
        print("Requested difficulty level: ", difficulty)
        # Try to redact the sudoku puzzle until a unique solution is found.
        while not successfull_redactions:
            redacted_grid = grid.copy()
            redacted_cells = 0
            checked_locations = []
            # Redact the sudoku puzzle by removing numbers.
            while redacted_cells <= (total_cells - cells_to_keep):
                # If the number of redacted cells is equal to the number of cells to redact, break the loop.
                if  redacted_cells == (total_cells - cells_to_keep):
                    best_attempt = redacted_grid.copy()
                    successfull_redactions = True
                    break
                i = random.randint(0, size - 1)
                j = random.randint(0, size - 1)
                # Check if the cell has already been checked.
                if (i, j) in checked_locations:
                    # If all cells have been checked and no unique solution is found, break the loop.
                    if len(checked_locations) == total_cells:
                        if redacted_cells >= best_attempt_redaction_count:
                            best_attempt_redaction_count = redacted_cells
                            best_attempt = redacted_grid.copy()
                        break
                    continue
                checked_locations.append((i, j))
                if redacted_grid[i][j] != 0:
                    last_removed = redacted_grid[i][j]
                    redacted_grid[i][j] = 0
                    redacted_cells += 1
                    if not self.check_unique_solution(redacted_grid, [i, j], last_removed):
                        redacted_cells -= 1
                        redacted_grid[i][j] = last_removed
                    else:
                        checked_locations = []
            attempts += 1
            # If 1000 attempts have been made, break the loop, give up and return the best attempt.
            if attempts > 10000:
                break
        
        # Print info about attempts and the best attempt.
        print("Number of redacted numbers: ", best_attempt_redaction_count)
        print("Requested number of redacted numbers: ", (total_cells - cells_to_keep))
        print("Number of attempts: ", attempts)
        return best_attempt   

    def print_sudoku(self, grid):
        """Print the sudoku grid in a readable format"""
        size = grid.shape[0]
        # Show separators between boxes if size is divisible by 3
        show_separators = size % 3 == 0
        box_size = 3 if show_separators else size
        
        number_redacted = 0
        for i in range(size):
            if show_separators and i % box_size == 0 and i != 0:
                print("------+-------+------")
            for j in range(size):
                if show_separators and j % box_size == 0 and j != 0:
                    print("|", end=" ")
                if grid[i][j] == 0:
                    print("_", end=" ")  
                    number_redacted +=1  
                else: 
                    print(grid[i][j], end=" ")
            print()
        if number_redacted > 0:
            print("Number of redacted numbers: ", number_redacted)
            print("Number of remaining numbers: ", size*size - number_redacted)

if __name__ == "__main__":

    sg = SudokuGenerator()
    sudoku9 = sg.generate_sudoku()
    redacted_sudoku9 = sg.redact_sudoku(sudoku9, 0.6)
    print("\n9x9 Grid:")
    sg.print_sudoku(sudoku9)
    print("\nRedacted 9x9 Grid:")
    sg.print_sudoku(redacted_sudoku9)