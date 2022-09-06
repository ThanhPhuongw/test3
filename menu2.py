import pygame_menu
import numpy as np
import pygame
import sys
import math

import playsound

from pygame_menu import Theme
from pygame_menu.examples import create_example_window
from typing import Tuple, Any, Optional, List


surface = create_example_window('CONNECT 4', (800, 800))
DIFFICULTY = ['EASY']
def music():
    pygame.mixer.init()
    pygame.mixer.music.load("mixkit-this-is-seeb-haus-631.mp3")
    pygame.mixer.music.play()



def set_difficulty(value: Tuple[Any, int], difficulty: str):
    """
    Change difficulty of the game.
    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = difficulty


VIOLET = (0,206,209)
BLACK = (0, 0, 0)
ORANGE = (255,255,255)
PINK = (255,0,0)
# rbg color

ROW_COUNT = 0
COLUMN_COUNT = 0


def start_the_game(difficulty: List):
    difficulty = difficulty[0]
    print(difficulty)

    music()

    if difficulty == "EASY":
        ROW_COUNT = 6
        COLUMN_COUNT = 7
    else:
        ROW_COUNT = 7
        COLUMN_COUNT = 8

    def create_board():
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(board, col):
        return board[ROW_COUNT - 1][col] == 0

    def draws(board):
        for c in range(COLUMN_COUNT):
            if board[ROW_COUNT - 1][c] == 0:
                return False
        return True

    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(board):
        print(np.flip(board, 0))

    def winning_move(board, piece):
        if difficulty == "EASY":
            for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT):
                    if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                        c + 3] == piece:
                        return True

            # Check vertical locations for win
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT - 3):
                    if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                        c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT - 3):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                            board[r + 3][c + 3] == piece:
                        return True

            # Check negatively sloped diaganols
            for c in range(COLUMN_COUNT - 3):
                for r in range(3, ROW_COUNT):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                            board[r - 3][c + 3] == piece:
                        return True
        else:
            # Check horizontal locations for win
            for c in range(COLUMN_COUNT - 4):
                for r in range(ROW_COUNT):
                    if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                        c + 3] == piece and board[r][c + 4] == piece:
                        return True

            # Check vertical locations for win
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT - 4):
                    if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                        c] == piece and board[r + 4][c] == piece:
                        return True

            # Check positively sloped diaganols
            for c in range(COLUMN_COUNT - 4):
                for r in range(ROW_COUNT - 4):
                    if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                            board[r + 3][c + 3] == piece and board[r + 4][c + 4]:
                        return True

            # Check negatively sloped diaganols
            for c in range(COLUMN_COUNT - 4):
                for r in range(2, ROW_COUNT):
                    if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                            board[r - 3][c + 3] == piece and board[r - 4][c + 4]:
                        return True

    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, VIOLET, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, ORANGE, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, PINK, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    # initalize pygame
    pygame.init()

    # define our screen size
    SQUARESIZE = 100

    # define width and height of board
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    #size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = create_example_window('PLAYING GAME', (height, width))
    # Calling function draw_board again
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, ORANGE, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render(f"{user_name1.get_value().upper()} wins!!", 1, ORANGE)
                            screen.blit(label, (40, 10))
                            game_over = True

                    if draws(board):
                        label = myfont.render("DRAWS!!", 1, ORANGE)
                        screen.blit(label, (40, 10))
                        game_over = True


                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render(f"{user_name2.get_value().upper()} wins!!", 1, PINK)
                            screen.blit(label, (40, 10))
                            game_over = True

                    if draws(board):
                        label = myfont.render("DRAWS!!", 1, PINK)
                        screen.blit(label, (40, 10))
                        game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
                    surface = create_example_window('CONNECT 4', (800, 800))


font = pygame_menu.font.FONT_FRANCHISE

myimage = pygame_menu.baseimage.BaseImage(
    image_path='257952647_1087561262058491_5657824237794059216_n.png',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)
my_theme = Theme(
    widget_font=font,
    background_color = myimage,
    widget_font_color = (0, 0, 0),
    selection_color = (255,0,0),
    widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(arrow_size=(15, 15), arrow_right_margin=5, arrow_vertical_offset=0, blink_ms=0),
    title_background_color = (102, 0, 102),
    title_font_color = (204,255,255)
)

menu = pygame_menu.Menu(
    height=800,
    theme=my_theme,
    title='CONNECT 4',
    width=800
)

menu1 = pygame_menu.Menu(
    height=800,
    theme=my_theme,
    title='Instruction',
    width=800
)
instruction = 'Players decide who goes first\n' \
              'Players must alternate turns. Only one piece is played at a time.\n'\
              'On your turn, drop one of your piece from the top into any of the columns. \n'\
              'The player who places 4 pieces in a row in a horizontal, vertical or diagonal row will wins\n'\
              'The game ends when there is a 4-in-a-row or a draw\n'

menu1.add.label(instruction, max_char=-1, font_size=25)
menu1.add.button('Return to main menu', pygame_menu.events.BACK)

user_name1 = menu.add.text_input('Name: ', default='Player 1')
user_name2 = menu.add.text_input('Name: ', default='Player 2')
menu.add.selector('Select difficulty ',
                  [('1 - Easy', 'EASY'),
                   ('2 - Hard', 'HARD')],
                  onchange=set_difficulty,
                  selector_id='select_difficulty')
menu.add.button('Play',
                start_the_game,
                DIFFICULTY)
menu.add.button('Instruction', menu1)
menu.add.button('Quit', pygame_menu.events.EXIT)

music()
if __name__ == '__main__':
    menu.mainloop(surface)

