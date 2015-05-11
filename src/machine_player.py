#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
from player import Player

class MachinePlayer(Player):
    BRAIN_LEVEL_0 = 0
    def __init__(self, role, name, level):
        super(MachinePlayer, self).__init__(role, name)
        self.level=level
        
    def make_decision(self, board, moves):
        sys.stdout.write('------------------------\n')
        board.dump(sys.stdout)
        sys.stdout.write('Possible Moves: ')
        for i in moves:
            sys.stdout.write(str(i))
        sys.stdout.write('\n')
        random.shuffle(moves)
        sys.stdout.write('{0} Choose: '.format(self.name))
        sys.stdout.write(str(moves[0]))
        sys.stdout.write('\n')
        return moves[0]
    
    def notify_diff(self, diffs):
        sys.stdout.write('Create Diffs: ')
        for i in diffs:
            sys.stdout.write(str(i))
        sys.stdout.write('\n')
