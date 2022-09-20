# coding:utf-8
import Chessman
import pygame


class Chessboard(object):

    def __init__(self, name):
        self.__name = name
        self.__is_red_turn = True
        self.__chessmans = [([None] * 9) for i in range(8)]
        self.__chessmans_hash = {}
        self.__history = {"red": {"chessman": None, "last_pos": None, "repeat": 0},
                          "black": {"chessman": None, "last_pos": None, "repeat": 0}}

    @property
    def is_red_turn(self):
        return self.__is_red_turn

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def chessmans(self):
        return self.__chessmans

    @property
    def chessmans_hash(self):
        return self.__chessmans_hash

    def init_board(self, screen):
        # pass
        for i in range(8):
            for j in range(9):
                pygame.draw.circle(screen, (138, 255, 255), (40 + 80*i, 40 + 80*j), 10)
        
    def add_chessman(self, chessman, col_num, row_num):
        self.chessmans[col_num][row_num] = chessman
        if chessman.name not in self.__chessmans_hash:
            self.__chessmans_hash[chessman.name] = chessman

    def remove_chessman_target(self, col_num, row_num):
        chessman_old = self.get_chessman(col_num, row_num)
        if chessman_old != None:
            self.__chessmans_hash.pop(chessman_old.name)

    def remove_chessman_source(self, col_num, row_num):
        self.chessmans[col_num][row_num] = None

    def calc_chessmans_moving_list(self):
        for chessman in self.__chessmans_hash.values():
            # if chessman.is_red == self.__is_red_turn:
            chessman.calc_moving_list()

    def clear_chessmans_moving_list(self):
        for chessman in self.__chessmans_hash.values():
            chessman.clear_moving_list()

    def move_chessman(self, chessman, col_num, row_num):
        if chessman.is_red == self.__is_red_turn:
            # self.remove_chessman_source(chessman.col_num, chessman.row_num)
            self.remove_chessman_target(col_num, row_num)
            self.add_chessman(chessman, col_num, row_num)
            self.__is_red_turn = not self.__is_red_turn
            return True
        else:
            print("the wrong turn")
            return False

    def update_history(self, chessman, col_num, row_num):
        red_or_black = self.red_or_black(chessman)
        history_chessman = self.__history[red_or_black]["chessman"]
        history_pos = self.__history[red_or_black]["last_pos"]
        if history_chessman == chessman and history_pos != None and history_pos[0] == col_num and history_pos[1] == row_num:
            self.__history[red_or_black]["repeat"] += 1
        else:
            self.__history[red_or_black]["repeat"] = 0
        self.__history[red_or_black]["chessman"] = chessman
        self.__history[red_or_black]["last_pos"] = (
            chessman.col_num, chessman.row_num)

    def red_or_black(self, chessman):
        if chessman.is_red:
            return "red"
        else:
            return "black"

    # def is_end(self):
    #     return self.who_is_victor(6)

    # def who_is_victor(self, repeat_num):
    #     whos_turn = "red" if self.__is_red_turn else "black"
    #     other_turn = "red" if not self.__is_red_turn else "black"
    #     chessman = self.get_chessman_by_name("{0}_king".format(whos_turn))
    #     if chessman != None:
    #         if self.__history[other_turn]["repeat"] == repeat_num:
    #             print("{0} is victor".format(whos_turn))
    #             return True
    #         else:
    #             return False
    #     else:
    #         print("{0} is victor".format(other_turn))
    #         return True

    def get_chessman(self, col_num, row_num):
        return self.__chessmans[col_num][row_num]

    def get_chessman_by_name(self, name):
        if name in self.__chessmans_hash:
            return self.__chessmans_hash[name]

    def get_top_first_chessman(self, col_num, row_num):
        for i in range(row_num + 1, 9, 1):
            current = self.chessmans[col_num][i]
            if current != None:
                return current

    def get_bottom_first_chessman(self, col_num, row_num):
        for i in range(row_num - 1, -1, -1):
            current = self.chessmans[col_num][i]
            if current != None:
                return current

    def get_left_first_chessman(self, col_num, row_num):
        for i in range(col_num - 1, -1, -1):
            current = self.chessmans[i][row_num]
            if current != None:
                return current

    def get_right_first_chessman(self, col_num, row_num):
        for i in range(col_num + 1, 8, 1):
            current = self.chessmans[i][row_num]
            if current != None:
                return current

    def get_top_second_chessman(self, col_num, row_num):
        count = 0
        for i in range(row_num + 1, 9, 1):
            current = self.chessmans[col_num][i]
            if current != None:
                if count == 1:
                    return current
                else:
                    count += 1

    def get_bottom_second_chessman(self, col_num, row_num):
        count = 0
        for i in range(row_num - 1, -1, -1):
            current = self.chessmans[col_num][i]
            if current != None:
                if count == 1:
                    return current
                else:
                    count += 1

    def get_left_second_chessman(self, col_num, row_num):
        count = 0
        for i in range(col_num - 1, -1, -1):
            current = self.chessmans[i][row_num]
            if current != None:
                if count == 1:
                    return current
                else:
                    count += 1

    def get_right_second_chessman(self, col_num, row_num):
        count = 0
        for i in range(col_num + 1, 8, 1):
            current = self.chessmans[i][row_num]
            if current != None:
                if count == 1:
                    return current
                else:
                    count += 1

    def print_to_cl(self):
        screen = "\r\n"
        for i in range(8, -1, -1):
            for j in range(8):
                if self.__chessmans[j][i] != None:
                    screen += self.__chessmans[j][i].name_cn
                else:
                    screen += "   .   "
            screen += "\r\n" * 3
        print(screen)

    def switch_turn_to_red(self):
        self.__is_red_turn = True

    def print_all_chessman_killing_list(self, screen):
        all_killing_list = []
        for i in range(8, -1, -1):
            for j in range(8):
                if self.__chessmans[j][i] != None:
                    if self.__chessmans[j][i].is_red == False:
                        self.__chessmans[j][i].calc_killing_list()
                        temp = self.__chessmans[j][i].killing_list
                        # print(self.__chessmans[j][i].name)
                        for point in temp:
                            [vc, vr] = [point.x, point.y]

                            # print(point.x, point.y, "\n")
                            if [vc, vr] not in all_killing_list:
                                all_killing_list.append([vc, vr])
        for point in all_killing_list:
            # print(point[0], point[1], "\n")
            pygame.draw.circle(screen, (138, 43, 226), (40 + 80*(point[0]) , 80*(8-point[1]) + 40), 10)
    
    def clear_all_chessman_killing_list(self, screen):
        for i in range(8, -1, -1):
            for j in range(8):
                pygame.draw.circle(screen, (138, 255, 255), (40 + 80*j , 80*(8-i) + 40), 10)

    def find_Red_Rook(self):
        for i in range(8, -1, -1):
            for j in range(8):
                if self.__chessmans[j][i] != None:
                    chessname = self.__chessmans[j][i].name
                    if "Red_rook" in chessname:
                        # chessman = self.__chessmans[j][i]
                        # print(chessman.col_num, chessman.row_num)
                        return self.__chessmans[j][i]
    def delete_chessman(self, col_num, row_num):
        chessman_at_position = self.get_chessman(col_num, row_num)
        if chessman_at_position != None:
            self.chessmans[col_num][row_num] = None
            self.__chessmans_hash.pop(chessman_at_position.name)


    def delete_chessman_in_a_row(self, row_num):
        for i in range(8):
            if self.__chessmans[i][row_num] != None and self.__chessmans[i][row_num].is_red == False:
                    self.delete_chessman(i, row_num)

    def delete_chessman_in_a_column(self, col_num):
        for i in range(8, -1, -1):
            if self.__chessmans[col_num][i] != None and self.__chessmans[col_num][i].is_red == False:
                    self.delete_chessman(col_num, i)


                

    
    




