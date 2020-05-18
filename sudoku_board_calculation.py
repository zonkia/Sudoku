from random import randint


def print_board(board):
    for row in board:
        print(row)


def convert_to_tuples(board):
    boardListOfTuples = []
    for row in board:
        boardListOfTuples.append(tuple(row))
    return tuple(boardListOfTuples)


def print_tuple(tupleBoard):
    for row in tupleBoard:
        print(row)


def convert_tuple_to_list(board):
    solution = []
    for row in board:
        solution.append(list(row))
    return solution

# ===========


class SolveSudoku:

    def __init__(self, board):
        solutions = []
        SolveSudoku.solve(self, board, solutions)
        try:
            self.solution = solutions[0]
        except:
            self.solution = None

    def solve(self, board, solutions):

        if SolveSudoku.check_if_complete(self, board):
            solutions.append(convert_to_tuples(board))
            return True

        if len(solutions) == 1:
            return solutions

        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    for number in range(1, 10):
                        if SolveSudoku.check_if_possible(self, board, number, y, x):
                            board[y][x] = number
                            SolveSudoku.solve(self, board, solutions)
                            board[y][x] = 0
                    return False

    def get_square_zero_coordinates(self, board, y, x):
        # check y
        if (y + 1)/3 <= 1:
            y0 = 0
        elif (y + 1)/3 > 1 and (y + 1)/3 <= 2:
            y0 = 3
        elif (y + 1)/3 > 2:
            y0 = 6
        # check x
        if (x + 1)/3 <= 1:
            x0 = 0
        elif (x + 1)/3 > 1 and (x + 1)/3 <= 2:
            x0 = 3
        elif (x + 1)/3 > 2:
            x0 = 6
        return [y0, x0]

    def get_square(self, board, squareCoordinates):
        row = []
        square = []
        y0 = squareCoordinates[0]
        x0 = squareCoordinates[1]
        for y in range(3):
            for x in range(3):
                row.append(board[y0 + y][x0 + x])
            square.append(row)
            row = []
        return square

    def get_column(self, board, x):
        column = []
        for row in board:
            column.append(row[x])
        return column

    def check_if_possible(self, board, num, y, x):
        if board[y][x] != 0:
            return False
        if num in board[y]:
            return False
        if num in SolveSudoku.get_column(self, board, x):
            return False
        square = SolveSudoku.get_square(
            self, board, SolveSudoku.get_square_zero_coordinates(self, board, y, x))
        for row in square:
            for number in row:
                if number == num:
                    return False
        return True

    def check_if_complete(self, board):
        for row in board:
            for number in row:
                if number == 0:
                    return False
        return True

    def get_possible_numbers(self, board, y, x):
        possibleNumbers = []
        for number in range(1, 10):
            if SolveSudoku.check_if_possible(self, board, number, y, x):
                possibleNumbers.append(number)
        return possibleNumbers


# ============================


class CreateSudoku:

    def __init__(self, level="easy"):

        solutions = []
        CreateSudoku.get_random_row(self,
                                    CreateSudoku.get_empty_row(self), solutions)
        board = CreateSudoku.get_random_board(self, list(solutions[0]))
        solutions = []
        SolveSudoku(board).solve(board, solutions)
        self.solution = solutions[0]
        self.readyBoard = []
        CreateSudoku.create_player_board(
            self, convert_tuple_to_list(self.solution), level)
        self.readyBoard = convert_tuple_to_list(self.readyBoard)

    def get_random_int(self):
        return randint(1, 9)

    def check_row(self, row):
        for number in row:
            if number == 0:
                return False
        return True

    def get_empty_row(self):
        row = [0
               for number in range(9)
               ]
        row[0] = CreateSudoku.get_random_int(self)
        return row

    def get_random_row(self, row, solutions):

        if CreateSudoku.check_row(self, row):
            solutions.append(tuple(row))
            return True

        if len(solutions) == 1:
            return solutions

        for position in range(9):
            number = CreateSudoku.get_random_int(self)
            if row[position] == 0 and number not in row:
                row[position] = number
                CreateSudoku.get_random_row(self, row, solutions)
                row[position] = 0
        return False

    def get_random_board(self, row):
        board = CreateSudoku.get_new_board(self)
        board[0] = row
        return board

    def get_new_board(self):
        return [[0
                 for _ in range(9)
                 ]
                for _ in range(9)
                ]

    def create_player_board(self, board, level):

        levels = {"easy": 30, "medium": 40, "hard": 50, "expert": 58}
        amountToGuess = levels[level]

        if CreateSudoku.check_empty_spaces(self, board, amountToGuess):
            self.readyBoard = convert_to_tuples(board)
            return True

        while CreateSudoku.check_empty_spaces(self, board, amountToGuess) == False:
            y = CreateSudoku.get_random_int(self) - 1
            x = CreateSudoku.get_random_int(self) - 1
            if board[y][x] == 0:
                continue
            else:
                board[y][x] = 0
                CreateSudoku.create_player_board(
                    self, board, level)

    def check_empty_spaces(self, board, amountToGuess):
        amountOfEmpty = 0
        for row in board:
            for number in row:
                if number == 0:
                    amountOfEmpty += 1
        if amountOfEmpty == amountToGuess:
            return True
        return False
