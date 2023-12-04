import pygame
from pygame.locals import *
import sys
from board import Board  # Replace 'board' with the actual name of your module

# Pygame initialization
pygame.init()

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 980
SCREEN_HEIGHT = 650

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('./res/background.jpg')
pygame.display.set_caption("Game Screen")
title = pygame.font.Font("./font/Sergio_Trendy.ttf", 40)
sub_title = pygame.font.Font("./font/Montserrat-Regular.ttf", 70)
font = pygame.font.Font("./font/Montserrat-Regular.ttf", 35)

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to run the Mahjong game
def run_mahjong_game():
    SCREEN_SIZE = 980, 650

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Mahjong')

    background = pygame.image.load('./res/background.jpg')
    gameover = pygame.image.load('./res/gameover.png')
    success = pygame.image.load('./res/success.png')
    replay = pygame.image.load('./res/restart.png') # 133, 30
    random = pygame.image.load('./res/random.png')
    undo = pygame.image.load('./res/undo.png') # 60, 60

    REPLAY = [133, 30]
    REPLAY_POS = [710, 565]

    UNDO =[60, 60]
    UNDO_POS = [915, 10]
    game_continue = True

    RANDOM = [133, 30]
    RANDOM_POS = [550, 565]

    while game_continue:

        board = Board()
        status = 0
        restart = False

        while True:

            screen.fill(0)
            screen.blit(background, (0, 0))
            screen.blit(replay, (REPLAY_POS[0], REPLAY_POS[1]))
            screen.blit(undo, (UNDO_POS[0], UNDO_POS[1]))
            screen.blit(random, (RANDOM_POS[0], RANDOM_POS[1]))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()  # mouse pos

                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index == 0:  # left
                                if position[0] >= REPLAY_POS[0] and position[0] <= REPLAY_POS[0] + REPLAY[0] and \
                                        position[1] >= REPLAY_POS[1] and position[1] <= REPLAY_POS[1] + REPLAY[1]:
                                    restart = True
                                    break
                                if position[0] >= UNDO_POS[0] and position[0] <= UNDO_POS[0] + UNDO[0] and \
                                        position[1] >= UNDO_POS[1] and position[1] <= UNDO_POS[1] + UNDO[1]:
                                    board.undo()
                                    break
                                if position[0] >= RANDOM_POS[0] and position[0] <= RANDOM_POS[0] + RANDOM[0] and \
                                        position[1] >= RANDOM_POS[1] and position[1] <= RANDOM_POS[1] + RANDOM[1]:
                                    board.shuffle_tiles()
                                    break
                                status = board.choose(position)
                            elif index == 2:  # right
                                status = board.pop(position)

            if restart:
                status = 0
                break

            board.display(screen)
            if status != 0:
                break

            pygame.display.update()

        if restart:
            continue

        if status == -1:
            screen.blit(gameover, ((SCREEN_WIDTH - gameover.get_width()) // 2, (SCREEN_HEIGHT - gameover.get_height()) // 2))
        if status == 1:
            screen.blit(success, ((SCREEN_WIDTH - success.get_width()) // 2, (SCREEN_HEIGHT - success.get_height()) // 2))
        pygame.display.update()

        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if position[0] >= REPLAY_POS[0] and position[0] <= REPLAY_POS[0] + REPLAY[0] and \
                            position[1] >= REPLAY_POS[1] and position[1] <= REPLAY_POS[1] + REPLAY[1]:
                        flag = False
                        game_continue = True
                        break

def show_instructions():
    show_instructions = True

    while show_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_instructions = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse is clicked in a specific area to exit
                if 690 < mouse_x < 780 and -10 < mouse_y < 20:
                    show_instructions = False

        screen.fill(0)
        screen.blit(background, (0, 0))

        draw_text(f"Instruksi", sub_title, BLACK, screen, 280, 100)
        draw_text("Cara Bermain", font, BLACK, screen, 200, 200)

        pygame.display.flip()

    # Ensure that the event queue is empty before exiting the function
    pygame.event.clear()

# Function to show the home screen
def show_home_screen():
    while True:
        screen.fill(0)
        screen.blit(background, (0, 0))

        # Text on the home screen
        draw_text("Selamat Datang di Game Mahjong", title, BLACK, screen, 150, 200)
        draw_text("Mulai Permainan", font, BLACK, screen, 360, 300)
        draw_text("Instuksi", font, BLACK, screen, 445, 350)
        draw_text("Keluar", font, BLACK, screen, 455, 400)

        # Update display
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse is clicked in the "Play Game" area
                if 360 < mouse_x < 530 and 300 < mouse_y < 340:
                    print("Play")
                    return True
                elif 400 < mouse_x < 585 and 350 < mouse_y < 380:
                    print("Instruction")
                    show_instructions()
                elif 455 < mouse_x < 585 and 400 < mouse_y < 440:
                    pygame.quit()
                    sys.exit()

# Main program
game_continue = True
while game_continue:
    mode = show_home_screen()

    if mode:
        run_mahjong_game()
        # Handle anything you need after the Mahjong game loop here

    # Reset the game_continue flag
    game_continue = False
