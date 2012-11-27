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

from settings import FREEMODE
from gameboard import Board
from common import nice_print
import pygame

class Freemode(object):
    def __init__(self,level,screensize):
        self.name = "Freemode"
        self.boardsize = screensize[1]-5
        self.level = level

        self.background_color = FREEMODE['bgcolor']
        self.background=pygame.Surface(screensize).convert()
        self.background.fill(self.background_color)

        self.board = Board(self.boardsize,level+2,4)
        self.board_rect = pygame.Rect((0,0),(self.boardsize,self.boardsize))

        self.changed = True

        for field in self.board.pygame_fields:
            field.update()
            self.background.blit(field.image,field.rect)

    def update(self):
        self.changed = False
        for field in self.board.pygame_fields:
            field.error_update()
            if field.changed:
                self.changed = True
                nice_print(["Field {0} changed".format(field.logicfield.get_coords()),
                            "Blitting on background."])

                field.update()
                self.background.blit(field.image,field.rect)

    def mousedown(self,pos):
        self.board.fieldclick(pos)

    def mouseup(self,pos):
        pass

    def done(self):
        if self.board.game_over():
            donetuple = ("freemode",self.level+1)
            return ("clicktocontinue",donetuple,"Click to continue")
        else:
            return False
