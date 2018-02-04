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
        (i, j) = choice([(i,j)])
