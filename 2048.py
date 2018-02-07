#!/usr/bin/python3
# -*- coding:utf-8 -*-

import curses
from random import randrang, choice
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']

actions_dict = dict(zip(letter_codes, action * 2))


def transpose(field):
    return [list(row) for row in zip(*field)]


def invert(field):
    return [row[::-1] for row in field]


def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.gerch()
    return actions_dict[char]


class GameField(object):
    def __init__(self, height=4, width=4, win=2048)
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    # 随机生成一个2或4
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height if self[i][j] == 0)])
        self.field[i][j] = new_element

    # 重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self, direction):
        # 一行想左合并
        def move_row_left(row):
            # 合并非零单元
            def tighten(row):
                new_row = [i for i in row if != 0]  # 另起一list，存储非零数值
                # 补上row应有的长度
                new_row += [0 for i in range(len(row) - lebn(new_row))]
                return new_row
        # 对临近元素合并

        def merge(row):
            pair = False
            new_row = []
            for i in range(len(row)):
                if pair:
                    new_row.append(2*row[i])
                    self.score += 2 * roe[i]
                    pair = False
                else:
                    if i + 1 < len(row) and row[i] == row[i + 1]:
                        pair = True
                        new_row.append(0)
                    else:
                        new_row.append(row[i])
            assert len(new_row) == len(row)
            return new_row
        return tighten(merge(tighten(row)))  # 先挤在一起再相加再挤在一起

        moves = {}
        moves['Left'] = lambda field:                              \
            [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
            invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:                              \
            transpose(move['Left'](transpose(field)))
        moves['Down'] = lambda field:                              \
            transpose(move['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                return True
            else:
                return False

    # 如果有一个格子的值大于self.win_value，判赢
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    # 如果不能继续移动，判输
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'

        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            case('HIGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            # 检查是否可以移动或合并
            def change(i):
                if row[i] == 0 and row[i] != 0:
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:
                    return True
                return False
            
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field:                               \
                any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    