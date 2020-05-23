from sudoku_board_calculation import *
import pygame
import sys
from pygame.locals import *
from math import floor, ceil
import time
from copy import deepcopy
from pprint import pprint

# resolution = (567 x 567)
# mousebox = (63 x 63)

windowSize = 81
windowMultiplier = 7
winWidth = int(windowSize * windowMultiplier)
winHeight = int(windowSize * windowMultiplier)
squareSize = int(windowSize * windowMultiplier / 3)
cellSize = int(squareSize / 3)
numberStep = round(cellSize / 3, 0)
hintStep = round(cellSize / 9, 0)

fpsClock = 30

# colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (150, 150, 150)
red = (220, 20, 60)
blue = (0, 0, 255)
green = (0, 128, 0)
gold = (179, 161, 111)
darkBlue = (40, 49, 74)

# global board declaration
playerFullBoard = []
playerGameBoard = []
playerGameBoardCopy = []

# global pressed keys declaration
pressedOkKeys = {}
pressedWrongKeys = {}

xNyN = []
xNyN2 = []


def start_game_choose_difficulty():
    global winWidth, winHeight, white, black, grey, fpsClock, allowedKeyValues, playerFullBoard, playerGameBoard, playerGameBoardCopy

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((winWidth, winHeight))
    display.fill(white)
    pygame.display.set_caption('Difficulty selection')

    mouseClicked = False
    mouseX = 0
    mouseY = 0
    pressed = ""

    global font, fontSize
    fontSize = 38
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    while True:
        display_level_selection(display)
        pygame.display.update()

        # get action made by player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
                if mouseX < winWidth / 2 - 100 or mouseY < 203.5 or \
                        mouseX > winWidth / 2 + 100 or mouseY > 363.5:
                    display.fill(white)
                    continue
                else:
                    display.fill(white)
                    display_menu_rectangles(mouseX, mouseY, display)

            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if mouseX < winWidth / 2 - 100 or mouseY < 203.5 or \
                        mouseX > winWidth / 2 + 100 or mouseY > 363.5:
                    display.fill(white)
                    continue
                else:
                    level = get_difficulty_level(mouseX, mouseY)
                    playerBoard = CreateSudoku(level)
                    playerFullBoard = convert_tuple_to_list(
                        playerBoard.solution)
                    playerGameBoard = playerBoard.readyBoard
                    playerGameBoardCopy = deepcopy(playerGameBoard)
                    main_game()

        display_level_selection(display)
        pygame.display.update()

    clock.tick(1)


def get_difficulty_level(mouseX, mouseY):
    if mouseY < 243.5:
        return "easy"
    elif mouseY >= 243.5 and mouseY < 283.5:
        return "medium"
    elif mouseY >= 283.5 and mouseY < 323.5:
        return "hard"
    elif mouseY >= 323.5:
        return "expert"


def display_menu_rectangles(mouseX, mouseY, display):
    global winWidth, gold

    boxX = winWidth / 2 - 100
    if mouseY < 243.5:
        boxY = 203.5
    elif mouseY >= 243.5 and mouseY < 283.5:
        boxY = 243.4
    elif mouseY >= 283.5 and mouseY < 323.5:
        boxY = 283.5
    elif mouseY >= 323.5:
        boxY = 323.5
    pygame.draw.rect(display, gold, (boxX, boxY, 200, 40), 3)


def display_level_selection(display, txtcolor=gold, bgcolor=white):
    global darkBlue
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render("Select difficulty:", True, darkBlue, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2 - 100)
    display.blit(text, textRect)

    text = font.render("Easy", True, txtcolor, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2 - 60)
    display.blit(text, textRect)

    text = font.render("Medium", True, txtcolor, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2 - 20)
    display.blit(text, textRect)

    text = font.render("Hard", True, txtcolor, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2 + 20)
    display.blit(text, textRect)

    text = font.render("Expert", True, txtcolor, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2 + 60)
    display.blit(text, textRect)


def main_game():
    global winWidth, winHeight, white, black, grey, fpsClock, allowedKeyValues, xNyN, xNyN2

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption('Sudoku')

    mouseClicked = False
    mouseX = 0
    mouseY = 0
    pressed = ""

    global font, fontSize
    fontSize = 38
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    while True:
        mouseClicked = False

        # get action made by player
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos

            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                mouseClicked = True
                click = event.button
                # draw clicked box and get return [boxX, boxY]
                clickedSquare = draw_clicked_box(mouseX, mouseY, display)
                pygame.display.update()

                # if left mouse button was pressed
                if click == 1:
                    y = mouseY
                    x = mouseX
                    wait_for_input_keyboard(
                        display, clickedSquare,  y, x)

                    if len(xNyN) > 0:
                        try:
                            mouseX = xNyN[0][0]
                            mouseY = xNyN[0][1]
                            xNyN = []
                        except:
                            xNyN = []
                            pass
                    elif len(xNyN2) > 0:
                        try:
                            mouseX = xNyN2[0][0]
                            mouseY = xNyN2[0][1]
                            xNyN2 = []
                        except:
                            xNyN2 = []
                            pass
                    # update sudoku view
                    display_playerBoard(display)
                    display_playerNumbers(display)
                    pygame.display.update()

                # if right mouse button was pressed
                elif click == 3:
                    y = mouseY
                    x = mouseX

                    # check if clicked square can be changed
                    boardCoordinates = get_board_y_x_from_clicked_square(
                        clickedSquare)
                    if playerGameBoardCopy[boardCoordinates[0]][boardCoordinates[1]] != 0:
                        display_text("CAN'T CHANGE THIS NUMBER", display)
                        pygame.display.update()
                        time.sleep(1)
                        continue

                    # delete previous number from pressedOkKeys and pressedWrongKeys
                    playerGameBoard[boardCoordinates[0]
                                    ][boardCoordinates[1]] = 0
                    if (clickedSquare[0], clickedSquare[1]) in pressedOkKeys:
                        del pressedOkKeys[(clickedSquare[0],
                                           clickedSquare[1])]
                    if (clickedSquare[0], clickedSquare[1]) in pressedWrongKeys:
                        del pressedWrongKeys[(
                            clickedSquare[0], clickedSquare[1])]

                    # get possible numbers for hint in current square
                    hint = get_allowed_answers(playerGameBoard, y, x)
                    display_hints(display, hint, y, x)
                    pygame.display.update()
                    wait_for_input_hint(display, clickedSquare, hint, y, x)

        # display sudoku
        display_playerBoard(display)
        draw_box(mouseX, mouseY, display)
        display_playerNumbers(display)
        pygame.display.update()

        # if board is correctly solved
        if check_if_board_solved(playerGameBoard) == True:
            while True:
                display_winnerBoard(display, background=gold, text="YOU WON!")
                time.sleep(10)

        clock.tick(fpsClock)


def wait_for_input_keyboard(display, clickedSquare,  y, x):
    global cellSize, xNyN, xNyN2

    xNyN = []
    xNyN2 = []

    upperLeftCoordinates = clickedSquare
    lowerRightCoordinates = [value + cellSize
                             for value in upperLeftCoordinates
                             ]
    while True:
        pygame.display.update()
        event = pygame.event.wait()
        draw_clicked_box(
            upperLeftCoordinates[0], upperLeftCoordinates[1], display)
        pygame.display.update()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # if event is keypress
        elif event.type == KEYDOWN:
            key = pygame.key.name(event.key)
            key = key.replace("[", "").replace("]", "")
            try:
                key = int(key)
            except:
                display_text("WRONG KEY", display)
                pygame.display.update()
                time.sleep(1)
                break

            boardCoordinates = get_board_y_x_from_clicked_square(clickedSquare)
            # check if chosen number CAN be changed
            if playerGameBoardCopy[boardCoordinates[0]][boardCoordinates[1]] != 0:
                display_text("CAN'T CHANGE THIS NUMBER", display)
                pygame.display.update()
                time.sleep(1)
                break

            # add number to player board
            playerGameBoard[boardCoordinates[0]][boardCoordinates[1]] = key
            operate_pressed_keys(key, clickedSquare, boardCoordinates)
            xNyN2.append((clickedSquare[0], clickedSquare[1]))
            return

        # if event is mousepress
        elif event.type == MOUSEBUTTONDOWN:
            remove_clicked_box(x, y, display)
            pygame.display.update()
            xn, yn = event.pos
            click = event.button

            if clickedSquare == draw_clicked_box(xn, yn, display):
                xNyN.append((xn, yn))
                return

            if click == 1 and clickedSquare != draw_clicked_box(xn, yn, display):

                wait_for_input_keyboard(
                    display, draw_clicked_box(xn, yn, display),  yn, xn)

            elif click == 3:

                # check if clicked square can be changed
                boardCoordinates = get_board_y_x_from_clicked_square(
                    clickedSquare)
                if playerGameBoardCopy[boardCoordinates[0]][boardCoordinates[1]] != 0:
                    display_text("CAN'T CHANGE THIS NUMBER", display)
                    pygame.display.update()
                    time.sleep(1)
                    break

                hint = get_allowed_answers(playerGameBoard, yn, xn)
                display_hints(display, hint, yn, xn)
                pygame.display.update()
                xNyN.append((xn, yn))
                wait_for_input_hint(display, draw_clicked_box(
                    xn, yn, display), hint, yn, xn)

            return


def wait_for_input_hint(display, clickedSquare, hint, y, x):
    global cellSize, xNyN

    upperLeftCoordinates = clickedSquare
    lowerRightCoordinates = [value + cellSize
                             for value in upperLeftCoordinates
                             ]

    display_playerBoard(display)
    display_playerNumbers(display)
    draw_clicked_box(x, y, display)
    display_hints(
        display, hint, y, x)
    pygame.display.update()

    while True:
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #  if event is keypress
        elif event.type == KEYDOWN:
            key = pygame.key.name(event.key)
            key = key.replace("[", "").replace("]", "")
            try:
                key = int(key)
            except:
                display_text("WRONG KEY", display)
                pygame.display.update()
                time.sleep(1)
                break
            # get board coordinates from clickedSquare coordinates
            boardCoordinates = get_board_y_x_from_clicked_square(clickedSquare)
            if playerGameBoard[boardCoordinates[0]][boardCoordinates[1]] != 0:
                display_text("CAN'T CHANGE THIS NUMBER", display)
                pygame.display.update()
                time.sleep(1)
                break
            # add number to player board
            playerGameBoard[boardCoordinates[0]][boardCoordinates[1]] = key
            operate_pressed_keys(key, clickedSquare, boardCoordinates)
            break

        #  if event is mouse movement
        elif event.type == MOUSEMOTION:
            mouseX, mouseY = event.pos
            # if mouse is outside clicked box
            if mouseX < upperLeftCoordinates[0] or \
                    mouseX > lowerRightCoordinates[0] - 1 or \
                    mouseY < upperLeftCoordinates[1] or \
                    mouseY > lowerRightCoordinates[1] - 1:
                continue
            # if mouse is inside clicked box
            else:
                display_playerBoard(display)
                display_playerNumbers(display)
                display_hints(
                    display, hint, y, x)
                draw_clicked_box(
                    upperLeftCoordinates[0], upperLeftCoordinates[1], display)
                # draw hintbox if there is hint value in the box
                if check_if_small_square_has_value(mouseX, mouseY, clickedSquare, hint):
                    draw_hint_box(mouseX, mouseY, display, clickedSquare, hint)
                pygame.display.update()
                continue

        #  if event is mouse press
        elif event.type == MOUSEBUTTONDOWN:
            try:
                # get key from pressed hint
                key = get_hint_value(display, hint, mouseY,
                                     mouseX, clickedSquare)
                # check if number CAN be changed
                boardCoordinates = get_board_y_x_from_clicked_square(
                    clickedSquare)
                if playerGameBoardCopy[boardCoordinates[0]][boardCoordinates[1]] != 0:
                    display_text("CAN'T CHANGE THIS NUMBER", display)
                    pygame.display.update()
                    time.sleep(1)
                    break
                # add number to player board
                playerGameBoard[boardCoordinates[0]][boardCoordinates[1]] = key
                operate_pressed_keys(key, clickedSquare, boardCoordinates)
            except:
                break
            break


def populateCells(display, number, x, y, color):
    cellSurf = font.render('%s' % (number), True, color)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    display.blit(cellSurf, cellRect)


def display_board(display, playerGameBoard, won=False):
    if won == True:
        color = black
    else:
        color = grey
    global cellSize, numberStep
    for y in range(9):
        for x in range(9):
            number = playerGameBoard[y][x]
            if number == 0:
                number = ""
            populateCells(display, number, int((x * cellSize) +
                                               numberStep), int((y * cellSize) + numberStep), color)


def display_text(string, display, won=False):
    if won == True:
        bgcolor = darkBlue
        txtcolor = white
        font = pygame.font.Font('freesansbold.ttf', 64)
    else:
        bgcolor = red
        txtcolor = black
        font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(string, True, txtcolor, bgcolor)
    textRect = text.get_rect()
    textRect.center = (winWidth // 2, winHeight // 2)
    display.blit(text, textRect)


def display_pressed_numbers(display, pressedKeys, wrong=False):
    global cellSize
    if wrong == False:
        color = green
    else:
        color = red
    for coordinates in pressedKeys:
        cellSurf = font.render('%s' % (pressedKeys[coordinates]), True, color)
        cellRect = cellSurf.get_rect()
        x = int(coordinates[0] + cellSize / 3)
        y = int(coordinates[1] + cellSize / 3)
        cellRect.topleft = (x, y)
        display.blit(cellSurf, cellRect)


def drawGrid(display, win=False):
    global winWidth, winHeight, cellSize, squareSize

    if win == True:
        color = black
    else:
        color = grey

    for x in range(0, winWidth, cellSize):
        pygame.draw.line(display, color, (x, 0), (x, winWidth))
    for y in range(0, winHeight, cellSize):
        pygame.draw.line(display, color, (0, y), (winHeight, y))

    for x in range(0, winWidth, squareSize):
        pygame.draw.line(display, black, (x, 0), (x, winWidth), 3)
    for y in range(0, winHeight, squareSize):
        pygame.draw.line(display, black, (0, y), (winHeight, y), 3)

    return None


def draw_box(mouseX, mouseY, display):
    global cellSize, winWidth, winHeight, red
    boxX = int(floor(mouseX / cellSize) * cellSize)
    boxY = int(floor(mouseY / cellSize) * cellSize)
    pygame.draw.rect(display, red, (boxX, boxY, cellSize, cellSize), 3)


def draw_clicked_box(mouseX, mouseY, display):
    global cellSize, winWidth, winHeight, blue
    boxX = int(floor(mouseX / cellSize) * cellSize)
    boxY = int(floor(mouseY / cellSize) * cellSize)
    pygame.draw.rect(display, blue, (boxX, boxY, cellSize, cellSize), 3)

    return [boxX, boxY]


def remove_clicked_box(mouseX, mouseY, display):
    global cellSize, winWidth, winHeight, black, white
    boxX = int(floor(mouseX / cellSize) * cellSize)
    boxY = int(floor(mouseY / cellSize) * cellSize)
    display.fill(white)
    drawGrid(display)
    display_board(display, playerGameBoard)
    display_pressed_numbers(display, pressedOkKeys)
    display_pressed_numbers(display, pressedWrongKeys, wrong=True)


def draw_hint_box(mouseX, mouseY, display, clickedSquare, hint):
    global cellSize, winWidth, winHeight, red
    hintSquareSize = int(cellSize / 3)
    boxX = int(floor(mouseX / hintSquareSize) * hintSquareSize)
    boxY = int(floor(mouseY / hintSquareSize) * hintSquareSize)
    pygame.draw.rect(
        display, red, (boxX, boxY, hintSquareSize, hintSquareSize), 3)


def check_if_small_square_has_value(mouseX, mouseY, clickedSquare, hint):
    global cellSize
    hintSquareSize = int(cellSize / 3)

    columns = len(hint)
    try:
        firstColumn = len(hint[0])
    except:
        firstColumn = 0
    try:
        secondColumn = len(hint[1])
    except:
        secondColumn = 0
    try:
        thirdColumn = len(hint[2])
    except:
        thirdColumn = 0

    xPosition = ceil((mouseX - clickedSquare[0] + 1) / hintSquareSize)
    yPosition = ceil((mouseY - clickedSquare[1] + 1) / hintSquareSize)

    if xPosition == 3 and columns < 3:
        return False
    if xPosition == 2 and columns < 2:
        return False

    if yPosition == 3 and firstColumn < 3 and secondColumn < 3 and thirdColumn < 3:
        return False
    if yPosition == 2 and firstColumn < 2 and secondColumn < 2 and thirdColumn < 2:
        return False

    if xPosition == 3 and yPosition == 3 and thirdColumn < 3:
        return False
    if xPosition == 3 and yPosition == 2 and thirdColumn < 2:
        return False

    if xPosition == 2 and yPosition == 3 and secondColumn < 3:
        return False
    if xPosition == 2 and yPosition == 2 and secondColumn < 2:
        return False

    return True


def get_board_y_x_from_clicked_square(clickedSquare):
    global cellSize

    if clickedSquare[0] == 0 and clickedSquare[1] == 0:
        y = 0
        x = 0
    elif clickedSquare[0] == 0:
        x = 0
        y = clickedSquare[1] / cellSize
    elif clickedSquare[1] == 0:
        y = 0
        x = clickedSquare[0] / cellSize
    else:
        y = clickedSquare[1] / cellSize
        x = clickedSquare[0] / cellSize

    return [int(y), int(x)]


def get_hint_value(display, hint, mouseY, mouseX, clickedSquare):
    global cellSize

    hintSquareSize = int(cellSize / 3)
    x = ceil((mouseX - clickedSquare[0] + 1) / hintSquareSize) - 1
    y = ceil((mouseY - clickedSquare[1] + 1) / hintSquareSize) - 1

    return hint[x][y]


def operate_pressed_keys(key, clickedSquare, boardCoordinates):
    global playerGameBoard, pressedOkKeys, pressedWrongKeys
    #  check if number is possible for solving the board
    if check_if_possible(playerGameBoard, key, boardCoordinates[0], boardCoordinates[1]) == True:
        if tuple(clickedSquare) in pressedWrongKeys:
            del pressedWrongKeys[tuple(clickedSquare)]
        pressedOkKeys[tuple(clickedSquare)] = key
    else:
        if tuple(clickedSquare) in pressedOkKeys:
            del pressedOkKeys[tuple(clickedSquare)]
        pressedWrongKeys[tuple(clickedSquare)] = key


def get_allowed_answers(playerGameBoard, mouseY, mouseX):
    global cellSize
    y = int(floor(mouseY / cellSize))
    x = int(floor(mouseX / cellSize))

    try:
        answerList = SolveSudoku(playerGameBoard).get_possible_numbers(
            playerGameBoard, y, x)
    except:
        answerList = []
    squareAnswer = []
    row = []
    for number in answerList:
        row.append(number)
        if len(row) == 3:
            squareAnswer.append(row)
            row = []

    total = 0
    for rows in squareAnswer:
        total += len(rows)

    if total < len(answerList):
        squareAnswer.append(row)

    return squareAnswer


def display_hints(display, hint, mouseY, mouseX):

    global cellSize, hintStep
    x = int(floor(mouseX / cellSize) * cellSize)
    y = int(floor(mouseY / cellSize) * cellSize)

    for row in range(len(hint)):
        for number in range(len(hint[row])):
            populate_hints(display, hint[row][number],
                           int((x + (row * cellSize / 3)) + hintStep),
                           int(y + (number * cellSize / 3) + hintStep))


def populate_hints(display, number, x, y):
    global fontSize
    smallFont = int(round(fontSize / 3, 0))
    font = font = pygame.font.Font('freesansbold.ttf', smallFont)
    cellSurf = font.render('%s' % (number), True, grey)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    display.blit(cellSurf, cellRect)


def display_playerBoard(display):
    global white, playerGameBoard
    display.fill(white)
    drawGrid(display)
    display_board(display, playerGameBoard)


def display_playerNumbers(display):
    global pressedOkKeys, pressedWrongKeys
    display_pressed_numbers(display, pressedOkKeys)
    display_pressed_numbers(display, pressedWrongKeys, wrong=True)


def display_winnerBoard(display, background=gold, text="YOU WON!"):
    global gold, pressedOkKeys, pressedWrongKeys, playerGameBoard
    display.fill(background)
    drawGrid(display, win=True)
    display_playerNumbers(display)
    display_board(display, playerGameBoard, won=True)
    display_text(text, display, won=True)
    pygame.display.update()


""" checking current number against whole board
"""


def count_occurance_in_list(listName, element):
    count = 0
    for number in listName:
        if element == number:
            count += 1

    return count


def get_square_zero_coordinates(board, y, x):
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


def get_square(board, squareCoordinates):
    square = []

    y0 = squareCoordinates[0]
    x0 = squareCoordinates[1]
    for y in range(3):
        for x in range(3):
            square.append(board[y0 + y][x0 + x])

    return square


def get_column(board, x):
    column = []
    for row in board:
        column.append(row[x])
    return column


def check_if_possible(board, num, y, x):

    if count_occurance_in_list(board[y], num) > 1:
        return False
    if count_occurance_in_list(get_column(board, x), num) > 1:
        return False
    if count_occurance_in_list(get_square(board, get_square_zero_coordinates(board, y, x)), num) > 1:
        return False

    return True


def check_if_board_solved(playerGameBoard):
    for y in range(9):
        for x in range(9):
            if playerGameBoard[y][x] == 0:
                return False
            if check_if_possible(playerGameBoard, playerGameBoard[y][x], y, x):
                continue
            else:
                return False

    return True


""" end of checking methods
"""


if __name__ == "__main__":
    start_game_choose_difficulty()
