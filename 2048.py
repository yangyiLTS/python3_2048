#!/usr/bin/python3
# -*- coding:utf-8 -*-

import curses
from random import randrange, choice
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']

actions_dict = dict(zip(letter_codes, actions * 2))

# 矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]

# 矩阵逆转
def invert(field):
    return [row[::-1] for row in field]


def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    # 随机生成一个2或4
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    # 重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        self.spawn() # 生成两个数字
        self.spawn()

    def move(self, direction):
        # 一行向左合并
        def move_row_left(row):
            # 合并非零单元
            def tighten(row):
                new_row = [i for i in row if i != 0]  # 另起一list，存储非零数值
                # 补上row应有的长度
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
        
            # 对临近元素合并
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2*row[i])
                        self.score += 2 * row[i]
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
        # 向左移动
        moves['Left'] = lambda field:                               \
            [move_row_left(row) for row in field]
        # 右移->矩阵逆置再左移
        moves['Right'] = lambda field:                              \
            invert(moves['Left'](invert(field)))
        # 上移->矩阵转置在左移
        moves['Up'] = lambda field:                                 \
            transpose(moves['Left'](transpose(field)))
        # 下移->矩阵转置再右移
        moves['Down'] = lambda field:                               \
            transpose(move['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
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

        # 在屏幕上输出一行
        def cast(string):
            screen.addstr(string + '\n')

        # 打印行与行之间的分隔线
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        # 打印数字和分隔符
        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            case('HIGHSCORE: ' + str(self.highscore))
        for row in self.field:
            # 打印每一行数字
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
            # 检查是否可以向左移动或合并
            def change(i):
                # 当连续两个相等时 或值为零的格子后面有一个非零格子 返回True
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False
            
            return any(change(i) for i in range(len(row) - 1))
        # 使用row_is_left_movable函数检查是否可以移动，与moves相似
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

def main(stdscr):
    
    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):
        game_field.draw(stdscr)

        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def game():
        game_field.draw(stdscr)
        
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): 
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    curses.use_default_colors()
    game_field = GameField(win=32)

    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)