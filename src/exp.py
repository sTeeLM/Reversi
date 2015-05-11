#!/usr/bin/python
# -*- coding: utf-8 -*-
class ReversiInvalidParam(Exception):
    def __init__(self, msg):
        self.msg = msg
        pass
    def __str__(self):
        return 'ReversiInvalidParam: '+ self.msg
    
class ReversiInvalidMove(Exception):
    def __init__(self, msg):
        pass
    def __str__(self):
        return 'ReversiInvalidMove: '+ self.msg    
