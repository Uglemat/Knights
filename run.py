#!/usr/bin/env python
from __future__ import print_function
from knights.game import Game


version = "2.2"

print("Launching game..  v", version)

game = Game()
game.loop()
