# coding:utf-8
import sys
import pygame
import random
import os.path
import Chessboard
import Point
import Chessman
from pygame.locals import *
import PySimpleGUI as sg

main_dir = os.path.split(os.path.abspath(__file__))[0]
SCREENRECT = Rect(0, 0, 640, 720)
winstyle=0
chess_id = 1

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'Img', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def select_sprite_from_group(sprite_group, col_num, row_num):
    for sprite in sprite_group:
        if sprite.chessman.col_num == col_num and sprite.chessman.row_num == row_num:
            return sprite


def translate_hit_area(screen_x, screen_y):
    return screen_x // 80, 8 - screen_y // 80




class Chessman_Sprite(pygame.sprite.Sprite):
    is_selected = False
    images = []
    is_transparent = False

    def __init__(self, images, chessman):
        pygame.sprite.Sprite.__init__(self)
        self.chessman = chessman
        self.images = images
        self.image = self.images[0]
        self.rect = Rect(chessman.col_num * 80,
                         (8 - chessman.row_num) * 80,  80,  80)

    def move(self, col_num, row_num):
        old_col_num = self.chessman.col_num
        old_row_num = self.chessman.row_num
        is_correct_position = self.chessman.move(col_num, row_num)
        if is_correct_position:
            self.rect.move_ip((col_num - old_col_num)
                              * 80, (old_row_num - row_num) * 80)
            self.rect = self.rect.clamp(SCREENRECT)
            self.chessman.chessboard.clear_chessmans_moving_list()
            self.chessman.chessboard.calc_chessmans_moving_list()
            return True
        return False

    def update(self):
        if self.is_selected:
            if self.is_transparent:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
            self.is_transparent = not self.is_transparent
        else:
            self.image = self.images[0]

def creat_sprite(sprite_group, chessmans_hash):
    for chessman in chessmans_hash.values():
        if isinstance(chessman, Chessman.Rec_button):
            images = load_images("button.gif", "transparent.gif")
        else:
            if chessman.is_red:
                if isinstance(chessman, Chessman.Rook):
                    images = load_images("red_rook.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Cannon):
                    images = load_images("red_cannon.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Knight):
                    images = load_images("red_knight.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.King):
                    images = load_images("red_king.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Elephant):
                    images = load_images("red_elephant.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Mandarin):
                    images = load_images("red_mandarin.gif", "transparent.gif")
                else:
                    images = load_images("red_pawn.gif", "transparent.gif")
                
            else:
                if isinstance(chessman, Chessman.Rook):
                    images = load_images("black_rook.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Cannon):
                    images = load_images("black_cannon.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Knight):
                    images = load_images("black_knight.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.King):
                    images = load_images("black_king.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Elephant):
                    images = load_images("black_elephant.gif", "transparent.gif")
                elif isinstance(chessman, Chessman.Mandarin):
                    images = load_images("black_mandarin.gif", "transparent.gif")
                else:
                    images = load_images("black_pawn.gif", "transparent.gif")

        chessman_sprite = Chessman_Sprite(images, chessman)
        sprite_group.add(chessman_sprite)

def add_sprite(sprite_group, name, col_num, row_num, cbd):
    if "Tướng" in name:
        new_chess_name = name
        new_chessman = Chessman.King(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_king.gif", "transparent.gif")
    elif "Sĩ" in name:
        new_chess_name = name
        new_chessman = Chessman.Mandarin(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_mandarin.gif", "transparent.gif")
    elif "Tượng" in name:
        new_chess_name = name
        new_chessman = Chessman.Elephant(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_elephant.gif", "transparent.gif")
    elif "Xe" in name:
        new_chess_name = name
        new_chessman = Chessman.Rook(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_rook.gif", "transparent.gif")
    elif "Pháo" in name:
        new_chess_name = name
        new_chessman = Chessman.Cannon(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_cannon.gif", "transparent.gif")
    elif "Mã" in name:
        new_chess_name = name
        new_chessman = Chessman.Knight(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_knight.gif", "transparent.gif")
    elif "Tốt" in name:
        new_chess_name = name
        new_chessman = Chessman.Pawn(new_chess_name, new_chess_name, False, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("black_pawn.gif", "transparent.gif")
    else: 
        new_chess_name = name
        new_chessman = Chessman.Rook(new_chess_name, new_chess_name, True, cbd)
        new_chessman.add_to_board(col_num, row_num)
        images = load_images("red_rook.gif", "transparent.gif")
    
    new_sprite = Chessman_Sprite(images, new_chessman)
    new_sprite.chessman.chessboard.clear_chessmans_moving_list()
    new_sprite.chessman.chessboard.calc_chessmans_moving_list()
    sprite_group.add(new_sprite)
    cbd.switch_turn_to_red()
    

def PopupWindow():

    #sg.theme('DarkAmber')   # Add a touch of color
    
    options = ['Tướng','Sĩ','Tượng', 'Xe', 'Pháo', 'Mã', 'Tốt', 'Red_rook']
    
    # All the stuff inside your window.
    layout = [ 
                [sg.Listbox(options,select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,size=(10,len(options)))],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]
    
    # Create the Window
    window = sg.Window('Make your choice', layout)
    
    # Event Loop to process "events" and get the "values" of the input
    while True:
        event, values = window.read()
        print( f"event={event}" )
        if event is None or event == 'Ok' or event == 'Cancel': # if user closes window or clicks cancel
            break
            
    # close  the window        
    window.close()
    
    if event == "Cancel":
        print( "You cancelled" )
        return None
    else:
        
        value = values[0]
        value1 = value[0]
        print('You entered ', value1)
        return value1   
def delete_sprite_in_a_row(not_this_col_num, row_num):
    for i in range(8):
        if i != not_this_col_num:
            chessman_sprite = select_sprite_from_group(
                        chessmans, i, row_num)
            if chessman_sprite != None:
                chessman_sprite.kill()
def delete_sprite_in_a_column(col_num, not_this_row_num):
    for i in range(8, -1, -1):
        if i != not_this_row_num:
            chessman_sprite = select_sprite_from_group(
                        chessmans, col_num, i)
            if chessman_sprite != None:
                chessman_sprite.kill()


pygame.init()
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
pygame.display.set_caption("Ky Phung Dich Thu")

# create the background, tile the bgd image
bgdtile = load_image('boardchess.gif')
background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))
pygame.display.flip()


cbd = Chessboard.Chessboard('000')
cbd.init_board(screen)

chessmans = pygame.sprite.Group()
framerate = pygame.time.Clock()

creat_sprite(chessmans, cbd.chessmans_hash)
current_chessman = None
cbd.calc_chessmans_moving_list()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if index == 0 and pressed_array[index]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col_num, row_num = translate_hit_area(mouse_x, mouse_y)
                    chessman_sprite = select_sprite_from_group(
                        chessmans, col_num, row_num)

                    if current_chessman is None:
                        if chessman_sprite is None:
                            new_chess = PopupWindow()
                            if new_chess != None:
                                new_chess = new_chess + str(chess_id)
                                add_sprite(chessmans, new_chess, col_num, row_num, cbd)
                                chess_id = chess_id + 1
                                current_chessman = None
                        else:
                            if chessman_sprite.chessman.is_red ==  cbd.is_red_turn:
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                    elif current_chessman != None:
                        if chessman_sprite != None:
                            if chessman_sprite.chessman.is_red == cbd.is_red_turn:
                                current_chessman.is_selected = False
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                            else:
                                success = current_chessman.move(
                                    col_num, row_num)
                                if success:
                                    chessmans.remove(chessman_sprite)
                                    chessman_sprite.kill()
                                    current_chessman.is_selected = False
                                    current_chessman = None
                        else:
                            success = current_chessman.move(col_num, row_num)
                            if success:
                                current_chessman.is_selected = False
                                current_chessman = None

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                print("you pressed SPACE")
                Red_Rook_chess = cbd.find_Red_Rook()
                col_num = Red_Rook_chess.col_num
                row_num = Red_Rook_chess.row_num
                # print(col_num, row_num)                
                cbd.delete_chessman_in_a_row(row_num)
                delete_sprite_in_a_row(col_num, row_num)
                cbd.delete_chessman_in_a_column(col_num)
                delete_sprite_in_a_column(col_num, row_num)
                cbd.switch_turn_to_black()



                


        framerate.tick(20)

        chessmans.clear(screen, background)

        # update all the sprites
        chessmans.update()        
        chessmans.draw(screen)
        cbd.clear_all_chessman_killing_list(screen)
        cbd.print_all_chessman_killing_list(screen)
        pygame.display.update()

# def main(winstyle=0):

#     pygame.init()
#     bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
#     screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
#     pygame.display.set_caption("中国象棋最强AI")

#     # create the background, tile the bgd image
#     bgdtile = load_image('boardchess.gif')
#     background = pygame.Surface(SCREENRECT.size)
#     for x in range(0, SCREENRECT.width, bgdtile.get_width()):
#         background.blit(bgdtile, (x, 0))
#     screen.blit(background, (0, 0))
#     pygame.display.flip()

#     cbd = Chessboard.Chessboard('000')
#     cbd.init_board()

#     chessmans = pygame.sprite.Group()
#     framerate = pygame.time.Clock()

#     creat_sprite_group(chessmans, cbd.chessmans_hash)
#     current_chessman = None
#     cbd.calc_chessmans_moving_list()
#     while not cbd.is_end():
#     #     for event in pygame.event.get():
#     #         if event.type == pygame.QUIT:
#     #             sys.exit()
#     #         elif event.type == MOUSEBUTTONDOWN:
#     #             pressed_array = pygame.mouse.get_pressed()
#     #             for index in range(len(pressed_array)):
#     #                 if index == 0 and pressed_array[index]:
#     #                     mouse_x, mouse_y = pygame.mouse.get_pos()
#     #                     col_num, row_num = translate_hit_area(mouse_x, mouse_y)
#     #                     chessman_sprite = select_sprite_from_group(
#     #                         chessmans, col_num, row_num)
#     #                     if current_chessman is None and chessman_sprite != None:
#     #                         if chessman_sprite.chessman.is_red == cbd.is_red_turn:
#     #                             current_chessman = chessman_sprite
#     #                             chessman_sprite.is_selected = True
#     #                     elif current_chessman != None and chessman_sprite != None:
#     #                         if chessman_sprite.chessman.is_red == cbd.is_red_turn:
#     #                             current_chessman.is_selected = False
#     #                             current_chessman = chessman_sprite
#     #                             chessman_sprite.is_selected = True
#     #                         else:
#     #                             success = current_chessman.move(
#     #                                 col_num, row_num)
#     #                             if success:
#     #                                 chessmans.remove(chessman_sprite)
#     #                                 chessman_sprite.kill()
#     #                                 current_chessman.is_selected = False
#     #                                 current_chessman = None
#     #                     elif current_chessman != None and chessman_sprite is None:
#     #                         success = current_chessman.move(col_num, row_num)
#     #                         if success:
#     #                             current_chessman.is_selected = False
#     #                             current_chessman = None
#         framerate.tick(20)
#         # clear/erase the last drawn sprites
#         chessmans.clear(screen, background)

#         # update all the sprites
#         chessmans.update()
#         chessmans.draw(screen)
#         pygame.display.update()


# if __name__ == '__main__':
#     main()
