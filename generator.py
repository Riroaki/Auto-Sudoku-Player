from itertools import chain
import random


class SudokuGenerator(object):
    """Generate sudoku games."""

    def generate(self, num_fill: int) -> tuple:
        assert 0 < num_fill < 81
        grids = [[] for _ in range(9)]
        solution = [[0 for _ in range(9)] for _ in range(9)]
        # Generate central grid
        grids[4] = list(range(1, 10))
        random.shuffle(grids[4])
        # Use matrix shift to expand central grid to around:
        # 0    1    2
        # ^    ^    ^
        # |    |    |
        # 3 <- 4 -> 5
        # |    |    |
        # v    v    v
        # 6    7    8
        grids[3], grids[5] = self._shift(grids[4], on_row=True)
        grids[1], grids[7] = self._shift(grids[4], on_row=False)
        grids[0], grids[6] = self._shift(grids[3], on_row=False)
        grids[2], grids[8] = self._shift(grids[5], on_row=False)
        # Fill grid to board
        for index in range(9):
            self._fill_grid(solution, index, grids[index])
        # Randomly choose cells to unmask as puzzle
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for _ in range(num_fill):
            while True:
                row, col = random.randint(0, 8), random.randint(0, 8)
                if puzzle[row][col] == 0:
                    puzzle[row][col] = solution[row][col]
                    break
        return puzzle, solution

    @staticmethod
    def _shift(grid: list, on_row: bool) -> tuple:
        # Shift on row / column
        matrix = [[grid[row * 3 + col] for col in range(3)] for row in
                  range(3)]
        # Order of shift
        order1, order2 = [1, 2, 0], [2, 0, 1]
        if random.random() < 0.5:
            order2, order1 = order1, order2
        if on_row:
            # Shifted matrix
            matrix1 = [matrix[index] for index in order1]
            matrix2 = [matrix[index] for index in order2]
        else:  # Shift on column
            matrix1 = [[0 for _ in range(3)] for _ in range(3)]
            matrix2 = [[0 for _ in range(3)] for _ in range(3)]
            for origin_col in range(3):
                shift_col1, shift_col2 = order1[origin_col], order2[origin_col]
                for row in range(3):
                    # Shifted matrix
                    matrix1[row][origin_col] = matrix[row][shift_col1]
                    matrix2[row][origin_col] = matrix[row][shift_col2]
        # Concatenate shifted matrix
        shift1, shift2 = list(chain(*matrix1)), list(chain(*matrix2))
        return shift1, shift2

    @staticmethod
    def _fill_grid(board: list, grid_index, grid: list) -> None:
        # Fill a list representing grid to game board
        for index in range(9):
            value = grid[index]
            row = grid_index // 3 * 3 + index // 3
            col = grid_index % 3 * 3 + index % 3
            board[row][col] = value
