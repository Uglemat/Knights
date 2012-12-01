#!/usr/bin/env python
from game.game import Game

version = "2.0"

print "Launching game..  v" + version

game = Game()
game.loop()
