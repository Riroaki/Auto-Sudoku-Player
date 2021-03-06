from copy import deepcopy
from itertools import permutations
from printer import print_sudoku


class SudokuSolver(object):
    """Solve sudoku puzzles."""

    # Store candidate solutions
    _possible_solutions = {}

    def solve(self, puzzle: list, show_progress: bool = False) -> list:
        board = [[int(puzzle[row][col]) for col in range(9)] for row in
                 range(9)]
        # Find solutions with solid evidence
        while True:
            step = 0
            # Detect each row, column and grid
            position_generators = [
                lambda row: [(row, col) for col in range(9)],
                lambda col: [(row, col) for row in range(9)],
                lambda grid: [(grid // 3 * 3 + i // 3,
                               grid % 3 * 3 + i % 3) for i in range(9)]]
            for get_positions in position_generators:
                for index in range(9):
                    all_positions = get_positions(index)
                    # Find all unknown positions
                    unknowns = list(
                        filter(lambda pos: board[pos[0]][pos[1]] == 0,
                               all_positions))
                    if len(unknowns) > 0:
                        # Count all digits' appear times
                        counter = [0 for _ in range(10)]
                        for row, col in all_positions:
                            counter[board[row][col]] += 1
                        # Find unused digits
                        unused = list(filter(lambda digit: counter[digit] == 0,
                                             range(1, 10)))
                        # Find all solutions for this row / column / grid
                        all_solutions = self._find_all_solutions(board,
                                                                 unknowns,
                                                                 unused)
                        # Find common matches in all solutions
                        moves = self._find_in_common(unknowns, all_solutions)
                        if len(moves) > 0:
                            step += len(moves)
                            for row, col, value in moves:
                                board[row][col] = value
                                # Print each step
                                if show_progress:
                                    print_sudoku(board)
            # No step could be derived: try a possible step
            if step == 0:
                # Remove already confirmed cells from possible solutions
                possible = {}
                for position, values in self._possible_solutions.items():
                    row, col = position
                    # Cell is not confirmed yet
                    if board[row][col] == 0:
                        # Only one candidate left
                        if len(values) == 1:
                            board[row][col] = list(values)[0]
                            step += 1
                            if show_progress:
                                print_sudoku(board)
                        else:
                            # Keep cells with multiple candidates
                            possible[position] = values
                self._possible_solutions = possible
            # backtracking
            if step == 0:
                # Stop trying if no possible solution could be derived
                if len(self._possible_solutions) == 0:
                    break
                # Sort possible solutions
                possible = sorted(self._possible_solutions.keys(),
                                  key=lambda k: len(
                                      self._possible_solutions[k]))
                # Start from cell with least possibilities
                position = possible[0]
                row, col = position
                for value in self._possible_solutions[position]:
                    # Generate another solver to deal with rest of the game
                    sub_solver = SudokuSolver()
                    board_copy = deepcopy(board)
                    board_copy[row][col] = value
                    try_solve = sub_solver.solve(board_copy, show_progress)
                    if self._valid_all(try_solve):
                        return try_solve
                # Still could not solve: stop trying
                break
        return board

    def _valid_one(self, puzzle: list, row: int, col: int) -> bool:
        # Validate row & column & grid of one cell
        grid = row // 3 * 3 + col // 3
        row_valid = self._valid_row(puzzle, row)
        col_valid = self._valid_col(puzzle, col)
        grid_valid = self._valid_grid(puzzle, grid)
        return row_valid and col_valid and grid_valid

    def _valid_all(self, puzzle: list) -> bool:
        # Validate all rows & columns and grids
        for index in range(9):
            if not self._valid_row(puzzle, index, strict=True) or \
                    not self._valid_col(puzzle, index, strict=True) or \
                    not self._valid_grid(puzzle, index, strict=True):
                return False
        return True

    @staticmethod
    def _valid_row(puzzle: list, row: int, strict: bool = False) -> bool:
        # Validate one row
        counter = [0 for _ in range(10)]
        for col in range(9):
            counter[puzzle[row][col]] += 1
        if strict and counter[0] != 0:
            return False
        return len(list(filter(lambda x: x > 1, counter[1:]))) == 0

    @staticmethod
    def _valid_col(puzzle: list, col: int, strict: bool = False) -> bool:
        # Validate one column
        counter = [0 for _ in range(10)]
        for row in range(9):
            counter[puzzle[row][col]] += 1
        if strict and counter[0] != 0:
            return False
        return len(list(filter(lambda x: x > 1, counter[1:]))) == 0

    @staticmethod
    def _valid_grid(puzzle: list, grid: int, strict: bool = False) -> bool:
        # Validate one grid
        counter = [0 for _ in range(10)]
        for index in range(9):
            row = grid // 3 * 3 + index // 3
            col = grid % 3 * 3 + index % 3
            counter[puzzle[row][col]] += 1
        if strict and counter[0] != 0:
            return False
        return len(list(filter(lambda x: x > 1, counter[1:]))) == 0

    def _find_all_solutions(self, puzzle: list, unknowns: list,
                            unfilled: list) -> list:
        assert len(unknowns) == len(unfilled)
        solutions = []
        # Generate permutations and select feasible solutions
        for sequence in permutations(unfilled):
            valid = True
            # Validate each cell
            for index in range(len(unknowns)):
                row, col = unknowns[index]
                puzzle[row][col] = sequence[index]
                if not self._valid_one(puzzle, row, col):
                    valid = False
                    break
            # Add feasible solution
            if valid:
                solutions.append(sequence)
            # Remember to clear cell's value
            for row, col in unknowns:
                puzzle[row][col] = 0
        return solutions

    def _find_in_common(self, positions: list, all_solutions: list) -> list:
        # Find what's in common in all solutions
        total = len(positions)
        common = []
        # Store all candidates and their appear times
        # in all solutions for each cell
        count = [{} for _ in range(total)]
        for solution in all_solutions:
            for index in range(total):
                value = solution[index]
                count[index][value] = count[index].get(value, 0) + 1
        # Check whether candidate is unique for each cell
        for index in range(total):
            candidate_dict = count[index]
            position = positions[index]
            # Extract cell with unique solution (which is the common solution)
            if len(candidate_dict) == 1:
                move = (*position, list(candidate_dict.keys())[0])
                common.append(move)
            else:
                # Store candidates into possible solutions
                values = set(candidate_dict.keys())
                if position in self._possible_solutions:
                    # Intersect if already exist
                    self._possible_solutions[position] = values.intersection(
                        self._possible_solutions[position])
                else:
                    self._possible_solutions[position] = values
        # Solution with solid evidence
        return common
