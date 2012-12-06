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
from modes.free_mode import Freemode
from knights.settings import SCOREMODE
from knights.settings import SIDEBAR

from knights.gui_elements import Sidebar
from knights.scores import submit_score, get_highscores
from knights.common import nice_print
import pygame

class Scoremode(Freemode):
    def __init__(self,level,screensize,score=0):
        super(Scoremode,self).__init__(level,screensize)
        self.name = "Scoremode"
        self.score = score
        self.prev_score = score
        self.base_score = SCOREMODE['base-score']
        self.clock = pygame.time.Clock()
        self.timeleft = (SCOREMODE['gametime']+1-0.001)*1000
        self.level = level

        sidebar_size = (screensize[0]-self.boardsize-SIDEBAR['board-padding'],
                        screensize[1])
        self.sidebar = Sidebar(self.score,sidebar_size,self.boardsize)
        self.sidebar_rect = self.sidebar.surface.get_rect()
        self.sidebar_rect = self.sidebar_rect.move((self.boardsize+SIDEBAR['board-padding'],0))

        self.pause = False
        self.pause_color      = SCOREMODE['pause-color']
        self.pause_alpha      = SCOREMODE['pause-alpha']
        self.pause_text       = SCOREMODE['pause-text']
        self.pause_text_color = SCOREMODE['pause-text-color']

        if self.level == 1:
            self.set_pause("Click to start game")

    def done(self):
        if self.board.game_over():
            timebonus = ((self.timeleft)*(self.level*self.level)*self.base_score)/20/1000
            next_round = ("scoremode",self.level+1,self.score+timebonus)

            close_call = {True: " ...Close call!", False: ""}[self.timeleft < 2000]

            messages = [
                (30,SCOREMODE['message-color'],"Level score: " + str(int(self.score-self.prev_score))),
                (30,SCOREMODE['message-color'],"Time left: " + "{0:.1f}".format(self.timeleft/1000) + " seconds"+close_call),
                (30,SCOREMODE['message-color'],"Timebonus: " + str(int(timebonus))),
                (45,SCOREMODE['message-important-color'],"Total score: " + str(int(self.score+timebonus))),
                (20,SCOREMODE['message-color'],"Click to continue to the next level...")]

            return ("clicktocontinue",next_round,messages)
        elif self.timeleft < 100:
            nice_print(["Writing score to file..."])

            hs = get_highscores(10)
            if not hs:
                max_hs = 0
                min_hs = 0
            else:
                max_hs = max(hs)
                min_hs = min(hs)

            if self.score > max_hs:
                highscore_message = (30,SCOREMODE['message-important-color'],"Congratulations! You broke the #1 highscore!")
            elif self.score > min_hs or len(hs) < 10:
                highscore_message = (30,SCOREMODE['message-color'],"Your score is in the top 10 highscores!")
            else:
                highscore_message = (30,SCOREMODE['message-color'],"You didn't get on the top 10 highscores.")

            submit_score(int(self.score))
            next_round = ("scoremode",1,0)
            messages = [(30,SCOREMODE['message-color'],"Game over!"),
                        (40,SCOREMODE['message-important-color'],"Final score: " + str(int(self.score))),
                        highscore_message,
                        (20,SCOREMODE['message-color'],"Click to start new game...")
                        ]
            return ("clicktocontinue_scoremode_loss",next_round,messages)
        else:
            return False

    def set_pause(self,text=False):
        if self.pause:
            self.reset()
            self.sidebar.update()
            return

        brx, bry = self.board_rect.size
        bry += 5

        font = pygame.font.SysFont("dejavuserif",55,bold=True)
        if not text:
            font = font.render(self.pause_text,
                               1,
                               self.pause_text_color)
        else:
            font = font.render(text,
                               1,
                               self.pause_text_color)
            
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

        self.sidebar.score_box.update("Score: "+str(int(self.sidebar.score)))
        self.sidebar.time_box.update("Time: "+str(int(self.timeleft/1000)))
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

        self.sidebar.mousedown(pos)

    def mouseup(self,pos):
        self.sidebar.mouseup(pos)

    def reset(self):
            self.pause = False
            self.background.fill(self.background_color)

            self.sidebar.reset()

            for field in self.board.pygame_fields:
                field.changed = True

    def button_clicked(self):
        for click in self.sidebar.button_clicked():
            yield click
