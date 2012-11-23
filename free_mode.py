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

        self.board = Board(self.boardsize,level+2,5)
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
                nice_print(["Field {} changed".format(field.logicfield.get_coords()),
                            "Blitting on background."])

                field.update()
                self.background.blit(field.image,field.rect)

    def mousedown(self,pos):
        self.board.fieldclick(pos)

    def done(self):
        if self.board.game_over():
            donetuple = ("freemode",self.level+1)
            return ("clicktocontinue",donetuple,"Click to continue")
        else:
            return False
