#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from player import Player
from exp import ReversiInvalidParam, ReversiInvalidMove
from debug import CheckerLog

logger = CheckerLog(sys.stdout)

class CheckerBoard(object):
    STATUS_IN_PROGRESS = 0
    STATUS_WHITE_WIN = 1
    STATUS_BLACK_WIN = 2
    STATUS_DRAW = 3
    BLACK_CHECK_PATTEN = re.compile(r'^bw+b.*')
    WHITE_CHECK_PATTEN = re.compile(r'^wb+w.*')
    
    class Diff(object):
        def __init__(self, x, y, f, t):
            self.x = x
            self.y = y
            self.f = f
            self.t = t
        def __str__(self):
            return '[x={0}, y={1}, {2}->{3}]'. \
                format(self.x, self.y, 
                       'b' if self.f == Player.PLAYER_BLACK else \
                       ('0' if self.f == 0 else 'w'), 
                       'b' if self.t == Player.PLAYER_BLACK else \
                       ('0' if self.t == 0 else 'w'))
    class Diffs(object):
        def __init__(self, left, right, up, down):
            self.left = left
            self.right = right
            self.up = up
            self.down = down
            self.diffs = []
        def push(self, diff):
            if not isinstance(diff, CheckerBoard.Diff):
                raise ReversiInvalidParam('pushed diff must be CheckerBoard.Diff')
            self.diffs.append(diff)
            return self
            
        def _val_direction_str(self, left, right, up, down):
            if (left, right, up, down) == (1, 0, 0, 0):
                return 'L'
            elif (left, right, up, down) == (0, 1, 0, 0):
                return 'R'
            elif (left, right, up, down) == (0, 0, 1, 0):
                return 'U'
            elif (left, right, up, down) == (0, 0, 0, 1):
                return 'D'
            elif (left, right, up, down) == (1, 0, 1, 0):
                return 'LU'
            elif (left, right, up, down) == (0, 1, 1, 0):
                return 'RU'
            elif (left, right, up, down) == (0, 1, 0, 1):
                return 'RD'
            elif (left, right, up, down) == (1, 0, 0, 1):
                return 'LD' 
            elif (left, right, up, down) == (0, 0, 0, 0):
                return 'C'
            else:
                raise ReversiInvalidParam('invalid direction')
        def __str__(self):
            tmp = '[{0}'.format(self.\
                                _val_direction_str(self.left, 
                                                   self.right,
                                                   self.up, 
                                                   self.down))
            for i in self.diffs:
                tmp+=str(i)
            tmp += ']'
            return tmp
    
    class Move(object):
        INVALID_POS = -1
        def __init__(self, role, x, y, skip=False):
            self.role = role;
            self.x = x
            self.y = y
            self.skip = skip
            if self.role != Player.PLAYER_WHITE and self.role != Player.PLAYER_BLACK:
                raise ReversiInvalidParam('invalid role')
        def __str__(self):
            return '[{0},{1},{2},{3}]'.format(
                    'b' if self.role == Player.PLAYER_BLACK else 'w',
                    'T' if self.skip else 'F',
                    self.x, self.y)
            
    def __init__(self, size, w_player, b_player):
        self.round = 1
        self.size = size
        self.w_player = w_player
        self.b_player = b_player
        if  not isinstance(self.w_player, Player) or \
            not isinstance(self.b_player, Player) or  \
            (w_player.role != Player.PLAYER_WHITE) or \
            (b_player.role != Player.PLAYER_BLACK) :
            raise ReversiInvalidParam('invalid player')
        if size <= 0:
            raise ReversiInvalidParam('invalid size')
        self.data_array = [[0 for i in xrange(0, size)] \
                           for j in xrange(0, size)]
        self.data_array[3][3] = Player.PLAYER_WHITE
        self.data_array[4][4] = Player.PLAYER_WHITE
        self.data_array[3][4] = Player.PLAYER_BLACK
        self.data_array[4][3] = Player.PLAYER_BLACK
        # 黑棋先行
        self.next_player = self.b_player
        self.status = CheckerBoard.STATUS_IN_PROGRESS

    def dump(self, fil):
        # status
        fil.write('+++status: {0}\n'.\
                  format(self._status_to_string(self.status)))
        # next player
        fil.write('+++next player: {0}\n'.format(
                self.next_player.name if self.next_player else 'None'))
        #round
        fil.write('+++round:{0}\n'.format(self.round))   
        # data array
        fil.write('+++checker board:\n')
        fil.write('+++ ')
        for i in xrange(0, self.size):
            fil.write('{0}'.format(i))
        fil.write('\n')
        for j in xrange(0, self.size):
            mystr='+++{0}'.format(j)
            for i in xrange(0, self.size):
                if self.data_array[i][j] == Player.PLAYER_WHITE:
                    mystr += 'w'
                elif self.data_array[i][j] == Player.PLAYER_BLACK:
                    mystr += 'b'
                else:
                    mystr += '0'
            mystr += '\n'
            fil.write(mystr)
        
    def run(self):
        while CheckerBoard.STATUS_IN_PROGRESS == self.status:
            diffs_list=[]
            moves = self.get_possible_moves(self.next_player)
            move = self.next_player.make_decision(self, moves)
            self.play(move, diffs_list).notify_diff(diffs_list)
        
    def play(self, move, diffs_list):
        # 一般合法性检查
        if not isinstance(move, CheckerBoard.Move):
            raise ReversiInvalidParam('move must be instance of CheckerBoard.Move')
        if self.next_player.role != move.role:
            raise ReversiInvalidMove('move.role must be next_player.role')
        if self.status != CheckerBoard.STATUS_IN_PROGRESS:
            raise ReversiInvalidMove('game already over')
        # 如果不是空步骤，并且不是可能的步骤
        if not move.skip and not self.\
        		_is_possible_move(move.x, move.y, move.role):
            raise ReversiInvalidMove('not a possible move')
        
        saved_player = self.next_player
        
        # 如果棋盘可以下一个子，但是尝试略过，是非法的
        tmp = self.get_possible_moves(self.next_player)
        if len(tmp) != 1 or not tmp[0].skip:
            if move.skip:
                raise ReversiInvalidMove('try to skip, but one can play')
         
        # 开始搞了    
        self.round += 1  
        r_player = self.b_player \
            if self.next_player is self.w_player else self.w_player
                
        # 如果不是空步骤
        if not move.skip:
            diffs_list.append(
                              CheckerBoard.Diffs(0,0,0,0).\
                              push(CheckerBoard.Diff(move.x, move.y,
                              self.data_array[move.x][move.y],
                              move.role)))
            self.data_array[move.x][move.y] = move.role
            # 下了个子，加一分
            self.next_player.score += 1
            # 翻转对手的棋子，更新两者的得分
            self._try_revert(move.x, move.y, self.next_player, \
                            r_player, diffs_list)
        else:
            pass
        
        # 转换角色
        self.next_player = r_player
        r_player = self.b_player \
            if self.next_player is self.w_player else self.w_player      
            
        # 如果本次是略过，并且另一方也没法走子了，结束STATUS_IN_PROGRESS
        tmp = self.get_possible_moves(self.next_player)
        if len(tmp) == 1 and tmp[0].skip and move.skip:
            self._end_progress(self.next_player, r_player)
        # 如果本次不是略过，并且另一方也没法走子了，并且下下次自己也没法走，结束STATUS_IN_PROGRESS
        elif len(tmp) == 1 and tmp[0].skip:
            tmp1 = self.get_possible_moves(r_player)
            if len(tmp1) == 1 and tmp1[0].skip:
                self._end_progress(self.next_player, r_player)
        # 如果棋盘满了，结束STATUS_IN_PROGRESS
        elif self.b_player.score + self.w_player.score == self.size ** 2:
                self._end_progress(self.next_player, r_player)
        
        return saved_player
        
    def _status_to_string(self, status):
        if status == CheckerBoard.STATUS_BLACK_WIN:
            return "Black Win"
        elif status == CheckerBoard.STATUS_WHITE_WIN:
            return "White Win"
        elif status == CheckerBoard.STATUS_IN_PROGRESS:
            return "In Progress"
        elif status == CheckerBoard.STATUS_DRAW:
            return "Draw"
        else:
            return "Unknown"
            
    def _end_progress(self, player, r_player):
        if self.next_player.score == r_player.score:
            self.status = CheckerBoard.STATUS_DRAW
        elif self.next_player.score > r_player.score:
            if self.next_player.role == Player.PLAYER_BLACK:
                self.status = CheckerBoard.STATUS_BLACK_WIN
            else:
                self.status = CheckerBoard.STATUS_WHITE_WIN
        else:
            if self.next_player.role == Player.PLAYER_BLACK:
                self.status = CheckerBoard.STATUS_WHITE_WIN
            else:
                self.status = CheckerBoard.STATUS_BLACK_WIN
        self.next_player = None
    
    def get_possible_moves(self, player):
        temp = []
        for x in xrange(0, self.size):
            for y in xrange(0, self.size):
                if self._is_possible_move(x, y, player.role):
                    temp.append(CheckerBoard.Move(player.role, x, y))
        if self.status == CheckerBoard.STATUS_IN_PROGRESS and not temp:
            temp.append(CheckerBoard.Move(player.role, 
                        CheckerBoard.Move.INVALID_POS,
                        CheckerBoard.Move.INVALID_POS, True))
        return temp
    
    def dup(self):
        wp = self.w_player.dup()
        bp = self.b_player.dup()
        ret = CheckerBoard(self.size, wp, bp)
        ret.status = self.status
        for i in xrange(0, self.size):
            for j in xrange(0, self.size):
                ret.data_array[i][j] = self.data_array[i][j]
        ret.next_player = wp if self.next_player == self.w_player else bp

    def _is_possible_move(self, x, y, role):
        # already have black or white
        if self.data_array[x][y] != 0:
            return False
        # test all directions: 
        return self._test_direction(x, y, role, 1, 0, 0, 0) or \
            self._test_direction(x, y, role, 1, 0, 1, 0) or \
            self._test_direction(x, y, role, 0, 0, 1, 0) or \
            self._test_direction(x, y, role, 0, 1, 1, 0) or \
            self._test_direction(x, y, role, 0, 1, 0, 0) or \
            self._test_direction(x, y, role, 0, 1, 0, 1) or \
            self._test_direction(x, y, role, 0, 0, 0, 1) or \
            self._test_direction(x, y, role, 1, 0, 0, 1)

    def _test_direction(self, x, y, role, left, right, up, down):
        temp = []
        temp.append(role)
        _x = x
        _y = y
        for i in xrange(0, self.size):
            if left:
                x -= 1
            if right:
                x += 1
            if up:
                y -= 1
            if down:
                y += 1
            if x >= self.size or x < 0 or y >= self.size or y < 0:
                break
            temp.append(self.data_array[x][y])
        ret = self._s_check(temp, role)
        logger.dbg('_test_direction {0} {1} {2} {3} {4} {5} {6} {7}'.
                   format(_x, _y, role, left, right, up, down, 
                          'OK' if ret else 'Fail'))
        return ret
    
    def _s_check(self, s, role):
        '''
        return true if s is [b, w, w...b, 0...] if role is b
        or s is [w, b, b...w, 0...] if role is w
        '''
        if not s or len(s) < 3:
            return False
        if role == Player.PLAYER_WHITE and s[0] != Player.PLAYER_WHITE or \
            role == Player.PLAYER_BLACK and s[0] != Player.PLAYER_BLACK:
            return False
        temp = ''
        for p in s:
            if p == Player.PLAYER_WHITE:
                temp += 'w'
            elif p == Player.PLAYER_BLACK:
                temp += 'b'
            else:
                temp += '0'
        if role == Player.PLAYER_WHITE and \
        		CheckerBoard.WHITE_CHECK_PATTEN.match(temp) \
            or role == Player.PLAYER_BLACK and \
            CheckerBoard.BLACK_CHECK_PATTEN.match(temp):
            logger.dbg('_s_check {0} {1} OK'.format(temp, role))
            return True
        logger.dbg('_s_check {0} {1} Fail'.format(temp, role))
        return False

    def _try_revert_direction(self, x, y, player, 
                              r_player, left, right, up, down, diffs_list):
        if self._test_direction(x, y, player.role, left, right, up, down):
            tmp = CheckerBoard.Diffs(left, right, up, down)
            _x = x
            _y = y
            for i in xrange(0, self.size):
                if left:
                    x -= 1
                if right:
                    x += 1
                if up:
                    y -= 1
                if down:
                    y += 1
                if x >= self.size or x < 0 or y >= self.size or y < 0:
                    break
                if not self._s_revert(x, y, player, r_player, tmp):
                    break
            diffs_list.append(tmp)
            
    def _try_revert(self, x, y, player, r_player, diffs_list):
        self._try_revert_direction(x, y, player, 
                                   r_player, 1, 0, 0, 0, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 1, 0, 1, 0, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 0, 0, 1, 0, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 0, 1, 1, 0, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 0, 1, 0, 0, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 0, 1, 0, 1, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 0, 0, 0, 1, diffs_list)
        self._try_revert_direction(x, y, player, 
                                   r_player, 1, 0, 0, 1, diffs_list)
 
    def _s_revert(self, x, y, player, r_player, diffs):
        if self.data_array[x][y] == r_player.role:
            logger.dbg('_s_revert: {0} {1} {2}->{3}'.\
                       format(x, y, self.data_array[x][y], player.role))
            self.data_array[x][y] = player.role
            player.score += 1
            r_player.score -= 1
            diffs.push(CheckerBoard.Diff(x, y, 
                                         r_player.role, player.role))
        elif self.data_array[x][y] == player.role:
            logger.dbg('_s_revert: {0} {1} {2}->{3} break'.\
                       format(x, y, self.data_array[x][y], player.role))
            return False
        else:
            logger.dbg('_s_revert: {0} {1} {2} break'.\
                       format(x, y, self.data_array[x][y]))
            return False
        return True
                
