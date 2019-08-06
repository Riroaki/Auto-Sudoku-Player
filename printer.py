def print_sudoku(game: list) -> None:
    # Print sudoku game
    print('-' * 19)
    for row in range(9):
        print('|', end='')
        for col in range(9):
            # Seperator of grid
            end = '|' if (col + 1) % 3 == 0 else ' '
            if game[row][col] == 0:
                print('.', end=end)
            else:
                print(game[row][col], end=end)
        print()
        # Print seperate line for a grid
        if (row + 1) % 3 == 0:
            print('-' * 19)
