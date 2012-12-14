#!/usr/bin/env python
"""
Copyright (C) 2012 Mattias Ugelvik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function
from knights.game import Game
from knights.meta import VERSION
from knights.args import do_stuff_with_args

do_stuff_with_args()

print("\nLaunching game..  v{0!s}".format(VERSION))

game = Game()
game.loop()
