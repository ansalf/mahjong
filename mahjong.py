import pygame
from pygame.locals import *
import sys
from board import Board

SCREEN_SIZE = 980, 650

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Mahjong')

background = pygame.image.load('./res/background.jpg')
gameover = pygame.image.load('./res/gameover.jpg')
success = pygame.image.load('./res/success_test.png')
replay = pygame.image.load('./res/replay.png') # 133, 30
undo = pygame.image.load('./res/undo_test.jpg') # 60, 60

REPLAY = [133, 30]
REPLAY_POS = [710, 565]

UNDO =[60, 60]
UNDO_POS = [915, 10]
game_continue = True


while game_continue:

    board = Board()
    status = 0
    restart = False
    
    while True:
        
        screen.fill(0)
        screen.blit(background, (0, 0))
        screen.blit(replay, (REPLAY_POS[0], REPLAY_POS[1]))
        screen.blit(undo, (UNDO_POS[0], UNDO_POS[1]))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                position = pygame.mouse.get_pos() # mouse pos

                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0: # left 
                            if position[0]>=REPLAY_POS[0] and position[0] <= REPLAY_POS[0]+REPLAY[0] and \
                               position[1]>=REPLAY_POS[1] and position[1] <= REPLAY_POS[1]+REPLAY[1]:
                                restart = True
                                break
                            if position[0]>=UNDO_POS[0] and position[0] <= UNDO_POS[0]+UNDO[0] and \
                               position[1]>=UNDO_POS[1] and position[1] <= UNDO_POS[1]+UNDO[1]:
                                board.undo()
                                break
                            status = board.choose(position)
                        elif index == 2: # right
                            status = board.pop(position)

        if restart:
            status = 0
            game_continue = True
            break

        board.display(screen)
        if status is not 0:
            break
        
        pygame.display.update()

    if restart:
        continue

    if status == -1:
        screen.blit(gameover, (100, 555))
    if status == 1:
        screen.blit(success, (400, 555))
    pygame.display.update()

    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if position[0]>=REPLAY_POS[0] and position[0] <=REPLAY_POS[0]+REPLAY[0] and \
                   position[1]>=REPLAY_POS[1] and position[1] <= REPLAY_POS[1]+REPLAY[1]:
                    flag = False
                    game_continue = True
                    break


