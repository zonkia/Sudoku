from sudoku_board_calculation import *

if __name__ == "__main__":

    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 0, 0, 4, 0, 2, 0, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    solution = SolveSudoku(board).solution
    print_board(convert_tuple_to_list(solution))
