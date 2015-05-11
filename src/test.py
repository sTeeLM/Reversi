#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from checker_board import CheckerBoard
from human_player import HumanPlayer
from machine_player import MachinePlayer
from player import Player

w_player = MachinePlayer(Player.PLAYER_WHITE, 
                         "Mr. White", MachinePlayer.BRAIN_LEVEL_0)
b_player = MachinePlayer(Player.PLAYER_BLACK, 
                         "Mr. Black", MachinePlayer.BRAIN_LEVEL_0)
#b_player = HumanPlayer(Player.PLAYER_BLACK, "Mr. Black")

cb = CheckerBoard(8, w_player, b_player)

cb.run()

print '----------------------FINAL-------------------'
cb.dump(sys.stdout)
print '{0} score {1}'.format(w_player.name, w_player.score)
print '{0} score {1}'.format(b_player.name, b_player.score)
