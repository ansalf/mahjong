import math
import os
import random

import pygame
from pygame.locals import *

# CONSTANTS
TOTALS = 137 # 8 * 17
ROW = 8
COL = 17
TILE_ROW = 50
TILE_COL = 64

class Tile:
    def __init__(self, name, img):
        self.name = name
        self.img = img



class Operation:
    def __init__(self, op_type, tile, list_pos=None):
        '''
        op_type - 'draw' or 'eliminate'
        list_pos - if type='eliminate', list_pos contains two positions (two eliminated)
                   if type='draw', list_pos contains one position (the draw one)
        '''
        if op_type in ['draw', 'eliminate']:
            self.type = op_type
        else:
            print('Operation type not found.')

        self.list_pos = list_pos
        self.tile = tile

    def get_pos(self):
        return self.list_pos
    
    def get_tile(self):
        return self.tile

    def get_type(self):
        return self.type


class Board:

    # def __init__(self):

    #     self.tile_in_hand = [] # tiles in hand
    #     self.tile_list = [] # tiles on board
    #     self.chosen = [] # tiles selected by player (two at most)
    #     self.op_history = [] # operation history

    #    # read all images
    #     files = os.listdir('./res/tile')
    #     for file in files:  # <-- Corrected line
    #         for i in range(4):
    #             path = os.path.join('./res/tile', file)
    #             try:
    #                 img = pygame.image.load(path)
    #             except pygame.error as e:
    #                 print(f"Error loading image {path}: {e}")
    #                 continue
    #             name = file.split('.')[0]
    #             tile = Tile(name, img)
    #             self.tile_list.append(tile)

    #     # shuffle and store in col_list
    #     random.shuffle(self.tile_list)
    #     self.col_list = []
    #     for i in range(0, len(self.tile_list), ROW):
    #         self.col_list.append(self.tile_list[i:i+ROW])
    def __init__(self):
        # Your existing initialization code
        self.tile_in_hand = []  # tiles in hand
        self.tile_list = []  # tiles on board
        self.chosen = []  # tiles selected by player (two at most)
        self.op_history = []  # operation history

        # Your existing code for reading and shuffling tiles
        files = os.listdir('./res/tile')
        for file in files:
            for i in range(4):
                path = os.path.join('./res/tile', file)
                try:
                    img = pygame.image.load(path)
                except pygame.error as e:
                    print(f"Error loading image {path}: {e}")
                    continue
                name = file.split('.')[0]
                tile = Tile(name, img)
                self.tile_list.append(tile)

        random.shuffle(self.tile_list)
        self.col_list = []
        for i in range(0, len(self.tile_list), ROW):
            self.col_list.append(self.tile_list[i:i + ROW])

    def shuffle_tiles(self):
        all_tiles = [tile for col in self.col_list for tile in col]
        random.shuffle(all_tiles)

        for col in range(len(self.col_list)):
            for row in range(len(self.col_list[col])):
                self.col_list[col][row] = all_tiles.pop()
            
    def display(self, screen):

        # board
        pos_row = 50
        for col in self.col_list:
            pos_col = 480
            for item in col:
                screen.blit(item.img, (pos_row, pos_col))
                pos_col -= TILE_COL
            pos_row += TILE_ROW

        # tile in hand
        pos_row = 400
        for tile in self.tile_in_hand:
            screen.blit(tile.img, (pos_row, 550))
            pos_row += TILE_ROW

        # chosen
        for pos in self.chosen:
            if pos[0] < 17:
                top_left = [(pos[0]+1) * 50, 544-(pos[1]+1)*64]
                pygame.draw.rect(screen, (255,0,0), (top_left[0], top_left[1], 50, 64), 5)
            elif pos[0] == 17:
                pygame.draw.rect(screen, (255,0,0), (400+pos[1]*50, 550 ,50 , 64), 5)



    def pop(self, pos):
        board_or_hand, col_index, row_index = self._list_position(pos)

        if board_or_hand == 1 and row_index == len(self.col_list[col_index])-1:
            
            # remove the drawed tile from chosen list
            tile = self.col_list[col_index].pop()
            while [col_index, row_index] in self.chosen:
                self.chosen.remove([col_index, row_index])
                
            self.tile_in_hand.append(tile)

            # update tile in hand
            updated, updated_tile_in_hand, repeat_index = self._update_in_hand()
            # self.tile_in_hand = self._update_in_hand()
            if updated == 1:
                self.tile_in_hand = updated_tile_in_hand
                self.op_history.append(Operation('eliminate', tile, [[col_index, row_index], [17, repeat_index]]))

            elif updated == 0:
                self.op_history.append(Operation('draw', tile, [col_index, row_index]))


            if self._check_succeed():
                print('Success!')
                return 1
            if self._check_fail():
                print('Failed!')
                return -1
        return 0


    def choose(self, pos):
        board_or_hand, col, row = self._list_position(pos)

        if board_or_hand == 1: # on board

            if len(self.chosen) < 2:
                self.chosen.append([col, row])
            elif len(self.chosen) == 2:
                self.chosen.pop(0)
                self.chosen.append([col, row])

        elif board_or_hand == 2: # on hand (col=17, row=hand_index)
            
            if len(self.chosen) < 2:
                self.chosen.append([col, row])
            elif len(self.chosen) == 2:
                self.chosen.pop(0)
                self.chosen.append([col, row])

        else:
            return 0
        
        self._eliminate_chosen()
        if self._check_succeed():
            print('Success!')
            return 1
        if self._check_fail():
            print('Failed!')
            return -1

        return 0


    def undo(self):
        
        # no history
        if len(self.op_history) == 0:
            return

        operation = self.op_history.pop()
        op_type = operation.get_type()
        if op_type == 'draw':
            pos_on_board = operation.get_pos()
            self.col_list[pos_on_board[0]].append(operation.get_tile())
            for i in range(len(self.tile_in_hand)):
                if self.tile_in_hand[i].name == operation.get_tile().name:
                    self.tile_in_hand.pop(i)


        elif op_type == 'eliminate':
            pos1 = operation.get_pos()[0]
            pos2 = operation.get_pos()[1]
            tile = operation.get_tile()

            # pos1
            if pos1[0] == 17: # in hand
                self.tile_in_hand.insert(pos1[1], tile)
            else: # on board
                self.col_list[pos1[0]].append(tile)
            
            # pos2
            if pos2[0] == 17:
                self.tile_in_hand.insert(pos2[1], tile)
            else:
                self.col_list[pos2[0]].append(tile)
    

    def get_len(self):
        return len(self.tile_list)

    
    def _eliminate_chosen(self):
        ''' update `list` self.chosen 
        NOTE: Eliminate two chosen tiles if they satisfy the rules.
        '''
        if len(self.chosen) < 2:
            return
        elif len(self.chosen) == 2:
            pos1 = self.chosen[0]
            pos2 = self.chosen[1]

            if pos1[0] == pos2[0]: # same col must be top two or on hand

                # in hand
                if pos1[0] == 17 and pos2[0] == 17:
                    if pos1[1] != pos2[1] and self.tile_in_hand[pos1[1]].name == self.tile_in_hand[pos2[1]].name:
                        new_in_hand = []
                        for i in range(len(self.tile_in_hand)):
                            if i != pos1[1] and i != pos2[1]:
                                new_in_hand.append(self.tile_in_hand[i])

                        e_tile = self.tile_in_hand[pos1[1]]
                        self.tile_in_hand = new_in_hand
                        self.chosen = []

                        # NOTE add history
                        self.op_history.append(Operation('eliminate', e_tile, list_pos=[pos1, pos2]))
                
                # not in hand
                else:
                    col_len = len(self.col_list[pos1[0]])
                    # if top two
                    if (pos1[1] == col_len-1 and pos2[1] == col_len-2) or \
                    (pos1[1] == col_len-2 and pos2[1] == col_len-1):
                        if self.col_list[pos1[0]][pos1[1]].name == self.col_list[pos2[0]][pos2[1]].name:
                            # pop top two
                            self.col_list[pos1[0]].pop()
                            e_tile = self.col_list[pos1[0]].pop()
                            self.chosen = []

                            # NOTE add history
                            self.op_history.append(Operation('eliminate', e_tile, list_pos=[pos1, pos2]))


            else: # different col

                # one in hand
                if pos1[0] == 17 or pos2[0] == 17:
                    if pos1[0] == 17:
                        hand_pos = [17, pos1[1]]
                        board_pos = [pos2[0], pos2[1]]
                    elif pos2[0] == 17:
                        hand_pos = [17, pos2[1]]
                        board_pos = [pos1[0], pos1[1]]

                    if board_pos[1] != len(self.col_list[board_pos[0]]) - 1:
                        return
                    else:
                        if self.tile_in_hand[hand_pos[1]].name == self.col_list[board_pos[0]][board_pos[1]].name:
                            e_tile = self.tile_in_hand.pop(hand_pos[1])
                            self.col_list[board_pos[0]].pop(board_pos[1])
                            self.chosen = []

                            # NOTE add history
                            self.op_history.append(Operation('eliminate', e_tile, list_pos=[board_pos, hand_pos]))

                # both on board
                else:

                    if pos1[1] != (len(self.col_list[pos1[0]]) - 1) or \
                    pos2[1] != (len(self.col_list[pos2[0]]) - 1):
                        return
                    else: # two head
                        if self.col_list[pos1[0]][pos1[1]].name == self.col_list[pos2[0]][pos2[1]].name:
                            self.col_list[pos1[0]].pop()
                            e_tile = self.col_list[pos2[0]].pop()
                            self.chosen = []

                            # NOTE add history
                            self.op_history.append(Operation('eliminate', e_tile, list_pos=[pos1, pos2]))
                                     


    def _list_position(self, position):
        ''' Return the list index according to position
        Arg - position returned by 'pygame.mouse.get_pos()' 
        Return - three element tuple (a, x, y)
               - a - 0 neither in hand or board
                   - 1 on board
                   - 2 in hand
               - x if a=1, index of the column if on board
                   if a=2, 17
               - y if a=1, index of the row if on board
                   if a=2, index of `list` tile_in_hand
        '''
        board_or_hand = 0 # board = 1, hand = 2, Neither = 0

        col = math.floor((position[0]-50)/TILE_ROW)
        row = math.floor((544 - position[1])/TILE_COL)

        if col >= 0 and row >= 0 and col < len(self.col_list) and \
            row < len(self.col_list[col]):

            board_or_hand = 1
            return (board_or_hand, col, row)
        
        else:
            if position[1] >= 550 and position[1] <= 550 + TILE_COL:
                index_in_hand = math.floor((position[0] - 400) / 50)
                if index_in_hand < len(self.tile_in_hand) and index_in_hand >= 0:
                    board_or_hand = 2
                    return (board_or_hand, 17, index_in_hand)
                else:
                    return (0, col, row)
    
            else:
                return (0, col, row)


    def _top(self, col_index):
        ''' Return the top tile of this column '''
        return self.col_list[col_index][len(self.col_list[col_index])-1]


    def _top_two_same(self, col_index):
        ''' check if this column has two same tiles on top '''
        length = len(self.col_list[col_index])
        if self.col_list[col_index][length-1].name == self.col_list[col_index][length-2].name:
            return True
        else:
            return False


    def _update_in_hand(self):
        '''Eliminate same tiles in the hand
        NOTE: There can only be two same tiles in the hand

        Return - `int`, `list`, `list`
        `int`   0 for no update, 1 for update
        `list`  updated list
        `int`  repeat index if updated
        '''

        tile_in_hand_new = []
        repeat_list = self._find_same_item(self.tile_in_hand)

        if len(repeat_list) == 0:
            return [0, self.tile_in_hand, 0]

        repeat1 = repeat_list[0][0]
        repeat2 = repeat_list[0][1]

        for index in range(len(self.tile_in_hand)):
            if index != repeat1 and index != repeat2:
                tile_in_hand_new.append(self.tile_in_hand[index])
        
        return [1, tile_in_hand_new, repeat1]
    

    def _check_fail(self):

        if len(self.tile_in_hand) > 3:
            return True
        if len(self.tile_in_hand) < 3:
            return False

        # top two same
        for col_index in range(COL):
            if(len(self.col_list[col_index])>1):
                if self._top_two_same(col_index):
                    return False

        top_and_hand = []

        num_in_hand = len(self.tile_in_hand)

        for col_index in range(COL):
            if len(self.col_list[col_index]) > 0:
                top_and_hand.append(self._top(col_index))
            else:
                top_and_hand.append(None)

        for tile in self.tile_in_hand:
            top_and_hand.append(tile)
        
        repeat_list = self._find_same_item(top_and_hand)

        # uncomment the follow code to print hint
        print(repeat_list)

        if len(self.tile_in_hand) == 3 and len(repeat_list) == 0:
            return True
        else:
            return False     


    def _check_succeed(self):
        for col in self.col_list:
            if len(col) > 0:
                return False
        if len(self.tile_in_hand) > 0:
            return False
        return True
        

    def _find_same_item(self, array):
        ''' get the same item in array
        Arg - `list`
        Return - `list`, every element is a `list` containing two index
        ''' 

        same_list = []
        # repeat1 = -1; repeat2 = -1
        for i in range(len(array)-1):
            if array[i] is None:
                continue
            for j in range(i+1, len(array)):
                if array[j] is None:
                    continue
                if array[i].name == array[j].name:
                    same_list.append([i, j])
        return same_list


    def _print_in_hand(self):
        for tile in self.tile_in_hand:
            print(tile.name)
        print('\n')
