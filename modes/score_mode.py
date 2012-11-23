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


from free_mode import Freemode
from settings import SCOREMODE
from settings import SIDEBAR

from gui_elements import Sidebar
from scores import submit_score
from common import nice_print
import pygame

class Scoremode(Freemode):
    def __init__(self,level,screensize,score=0):
        super(Scoremode,self).__init__(level,screensize)
        self.name = "Scoremode"
        self.score = score
        self.base_score = SCOREMODE['base-score']
        self.clock = pygame.time.Clock()
        self.timeleft = (51-(5*(level/3)))*1000

        self.level = level


        sidebar_size = (screensize[0]-self.boardsize-SIDEBAR['board-padding'],screensize[1])
        self.sidebar = Sidebar(self.score,sidebar_size)
        self.sidebar_rect = self.sidebar.surface.get_rect()
        self.sidebar_rect = self.sidebar_rect.move((self.boardsize+SIDEBAR['board-padding'],0))

        self.pause = False
        self.pause_color = SCOREMODE['pause-color']
        self.pause_alpha = SCOREMODE['pause-alpha']
        self.pause_text =  SCOREMODE['pause-text']

    def done(self):
        if self.board.game_over():
            timebonus = ((self.timeleft)*(self.level*self.level)*self.base_score)/20/1000
            next_round = ("scoremode",self.level+1,self.score+timebonus)
            return ("clicktocontinue",next_round,"Click to continue")
        elif self.timeleft < 100:
            nice_print(["Writing score to file..."])
            submit_score(self.score)
            next_round = ("scoremode",1,0)
            return ("clicktocontinue_scoremode_loss",next_round,"You lost! Click to play again")
        else:
            return False

    def set_pause(self):
        if self.pause:
            self.reset()
            self.sidebar.update()
            return

        brx, bry = self.board_rect.size

        font = pygame.font.SysFont("dejavuserif",
                                   55,
                                   bold=True)
        font = font.render(self.pause_text,1,(250,242,0))
        renderpos = font.get_rect(centerx=brx/2,centery=bry/2)

        pause_background = pygame.Surface((brx,bry))
        pause_background.set_alpha(self.pause_alpha)
        pause_background.fill(self.pause_color)
        pause_background.blit(font, renderpos)
        self.background.blit(pause_background,(0,0))
        self.pause = True

    def update(self):
        if not self.pause:
            super(Scoremode,self).update()
            self.timeleft -= self.clock.tick()
        else:
            self.clock.tick()
            self.changed = False
        self.sidebar.score = self.score

        self.sidebar.score_box.update("Score: "+str(self.sidebar.score))
        self.sidebar.time_box.update("Time: "+str(self.timeleft/1000))
        self.sidebar.level_box.update("Level: "+str(self.level))

        if self.sidebar.changed:
            self.changed = True
            nice_print(["Sidebar changed:",
                        "Blitting on background."])
            self.background.blit(self.sidebar.surface,self.sidebar_rect)
        self.sidebar.update()

    def mousedown(self,pos):
        if self.pause and self.board_rect.collidepoint(pos):
            self.reset()
            self.background.fill(self.background_color)
            self.sidebar.update()
            for field in self.board.pygame_fields:
                field.changed = True
            self.changed = True
            self.pause = False
        else:
            field_type = self.board.fieldclick(pos)
            if field_type == "open":
                self.score += self.base_score * self.level
                nice_print(["Score increased to:",str(self.score)])

        self.sidebar.mousedown(pos,self.boardsize)

    def reset(self):
            self.pause = False
            self.background.fill(self.background_color)

            self.sidebar.reset()

            for field in self.board.pygame_fields:
                field.changed = True

    def button_clicked(self):
        for click in self.sidebar.button_clicked():
            yield click
