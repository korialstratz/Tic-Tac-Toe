import pygame as pg, sys
from pygame.locals import *
import time

# Game variables
xo = "x"
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (189, 118, 47)

# Game Board

board = [[None]*3, [None]*3, [None]*3]

# initializing window

pg.init()
fps = 30
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic-Tac-Toe")

# Game images

opening = pg.image.load("game images/Open.png")
x_img = pg.image.load("game images/X-rem.png")
o_img = pg.image.load("game images/O-rem.png")
wood = pg.image.load("game images/wood.jpg")

x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))
wood = pg.transform.scale(wood, (width, height + 100))


def game_opening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    screen.blit(wood, (0, 0))

    # vertical line
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3*2, 0), (width / 3*2, height), 7)

    # horizontal line
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3*2), (width, height / 3*2), 7)

    draw_status()


def draw_status():
    global draw

    if winner is None:
        message = xo.upper() + " 's Turn"
    else:
        message = winner.upper() + " won!"

    if draw:
        message = "It's a Draw!"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (0, 0, 0))

    screen.blit(wood, (0, 400, 500, 100))
    pg.draw.line(screen, line_color, (0, 403), (width, 403), 7)
    text_rect = text.get_rect(center=(width / 2, height+50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw

    # check for row
    for row in range(0,3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1)*height / 3 - height / 6),
                         (width, (row + 1 )*height / 3 - height / 6), 4)
            break

    # check for col
    for col in range(0,3):
        if (board[col][0] == board[col][1] == board[col][2]) and (board[col][0] is not None):
            winner = board[col][0]
            pg.draw.line(screen, (250, 0, 0), (0, (col + 1)*width / 3 - width / 6),
                         (width, (col + 1 )*width / 3 - width / 6), 4)
            break

    # check for diagonal
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all(all(row) for row in board) and winner is None:
        draw = True
    draw_status()


def draw_xo(row, col):
    global board, xo
    if row == 1:
        posx = 30
    if row == 2:
        posx = width/3 + 30
    if row == 3:
        posx = width/3*2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height/3 + 30
    if col == 3:
        posy = height/3*2 + 30

    board[row-1][col-1] = xo

    if xo == "x":
        screen.blit(x_img, (posy, posx))
        xo = "o"
    else:
        screen.blit(o_img, (posy,posx))
        xo = "x"
    pg.display.update()


def user_click():
    # mouse coordinates
    x,y = pg.mouse.get_pos()

    # get clicked column
    if x < width/3:
        col = 1
    elif x < width/3*2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # get clicked row
    if y < height/3:
        row = 1
    elif y < height/3*2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and board[row-1][col-1] is None:
        global xo

        draw_xo(row, col)
        check_win()


def reset_game():
    global board, winner, xo, draw
    time.sleep(3)
    xo = "x"
    draw = False
    game_opening()
    winner = None
    board =[[None]*3, [None]*3, [None]*3]


game_opening()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if winner or draw:
                reset_game()

    pg.display.update()
    clock.tick(fps)
