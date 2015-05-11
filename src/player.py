#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from exp import ReversiInvalidParam
class Player(object):
    PLAYER_WHITE = 1
    PLAYER_BLACK = 2
    def __init__(self, role, name):
        self.role = role;
        if self.role != Player.PLAYER_WHITE and \
        	self.role != Player.PLAYER_BLACK:
            raise ReversiInvalidParam
        self.score = 2
        self.name = name

    def dup(self):
        ret = Player(self.role)
        ret.score = self.score
        return ret
    
    def notify_diff(self, diffs):
        pass
