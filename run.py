#!/usr/bin/env python
from __future__ import print_function
from knights.game import Game
from knights.settings import VERSION
from knights.args import in_lack_of_a_better_function_name___do_stuff_with_args

in_lack_of_a_better_function_name___do_stuff_with_args()
print("\nLaunching game..  v{0!s}".format(VERSION))

game = Game()
game.loop()
