#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from player import Player
from checker_board import CheckerBoard

class HumanPlayer(Player):
    def __init__(self, role, name):
        super(HumanPlayer, self).__init__(role, name)
        
    def make_decision(self, board, moves):
        sys.stdout.write('Possibel Moves: ')
        for i in moves:
            i.dump(sys.stdout)
        sys.stdout.write('\n')
        (x, y) = sys.stdin.readline().strip().split(' ')
        x = int(x)
        y = int(y)
        if x != -1 and y != -1:
            return CheckerBoard.Move(self.role, x, y)
        else:
            return CheckerBoard.Move(self.role, x, y, True)
