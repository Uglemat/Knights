#!/usr/bin/env python
from __future__ import print_function
from knights.game import Game
from knights.settings import VERSION

print("Launching game..  v{0!s}".format(VERSION))

game = Game()
game.loop()
