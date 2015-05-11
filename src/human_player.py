#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from player import Player
from checker_board import CheckerBoard

class HumanPlayer(Player):
    def __init__(self, role, name):
        super(HumanPlayer, self).__init__(role, name)
        
    def make_decision(self, board, moves):
        sys.stdout.write('------------------------\n')
        board.dump(sys.stdout)
        sys.stdout.write('Possible Moves: ')
        for i in moves:
            sys.stdout.write(str(i))        
        sys.stdout.write('\n')
        (x, y) = sys.stdin.readline().strip().split(' ')
        x = int(x)
        y = int(y)
        if x != -1 and y != -1:
            return CheckerBoard.Move(self.role, x, y)
        else:
            return CheckerBoard.Move(self.role, x, y, True)
        
    def notify_diff(self, diffs):
        sys.stdout.write('Create Diffs: ')
        for i in diffs:
            sys.stdout.write(str(i))
        sys.stdout.write('\n')