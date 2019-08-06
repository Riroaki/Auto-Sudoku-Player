import sys
from generator import SudokuGenerator
from solver import SudokuSolver
from printer import print_sudoku


def test(num_fill: int):
    generator = SudokuGenerator()
    solver = SudokuSolver()
    # Generate a puzzle with solution
    puzzle, solution = generator.generate(num_fill)
    # Print puzzle
    print('Puzzle:')
    print_sudoku(puzzle)
    # Print solution
    print('Solution:')
    print_sudoku(solution)
    # Solve problem with progress shown
    print('Solved:')
    solution_solved = solver.solve(puzzle, show_progress=True)
    # Print final stage
    print_sudoku(solution_solved)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        num = 40
    else:
        num = int(sys.argv[1])
    test(num)
