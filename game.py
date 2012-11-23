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

import pygame

from settings import GAME
from common import nice_print

from modes.mainmenu_mode import Mainmenu
from modes.score_mode import Scoremode
from modes.clicktocontinue_mode import ClickToContinue
from modes.highscore_mode import Highscore

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode(GAME['resolution'])
        pygame.display.set_caption(GAME['caption'])
        self.clock = pygame.time.Clock()
        self.timeinterval = GAME['fps-limit']

        self.mode = Mainmenu(self.screen.get_size())

    def loop(self):
        while 1:
            self.handle_button_clicks()

            self.modeswitch(self.mode.done())
            self.events()

            self.blit()
            self.update()

            pygame.display.flip()
            self.clock.tick(self.timeinterval)

    def handle_button_clicks(self):
        if self.mode.name == "Scoremode":
            buttons = self.mode.button_clicked()
            for name in buttons:
                if name == "quit":
                    nice_print(["Game.handle_button_clicks:",
                                "'quit' clicked: exiting"])
                    exit()
                elif name == "restart":
                    self.mode = Scoremode(1,self.screen.get_size())

                elif name == "pause":
                    self.mode.set_pause()

                elif name == "main_menu":
                    self.mode = Mainmenu(self.screen.get_size())

        elif self.mode.name == "Mainmenu":
            buttons = self.mode.button_clicked()
            for name in buttons:
                if name == "scoremode":
                    self.mode = Scoremode(1,self.screen.get_size())
                elif name == "exit":
                    nice_print(["Game.handle_button_clicks:",
                                "'quit' clicked: exiting"])
                    exit()
                elif name == "highscore":
                    self.mode = Highscore(self.screen.get_size())

    def blit(self):
        if self.mode.changed:
            nice_print(["Mode {!r} changed:".format(self.mode.name),
                        "Blitting on screen\n"])
            self.screen.blit(self.mode.background,(0,0))


    def update(self):
        self.mode.update()

    def events(self):
        for i in pygame.event.get():
            if i.type==pygame.QUIT or i.type==pygame.KEYDOWN and i.key==pygame.K_ESCAPE:
                exit()
            if i.type==pygame.MOUSEBUTTONDOWN:
                self.mode.mousedown(i.pos)

    def modeswitch(self,done): # done is tuple with necessary information
        if done:
            self.blit()
            self.mode.update()
            self.blit()
            newmode = done[0]
            if newmode == "freemode":
                self.mode = Freemode(done[1],self.screen.get_size())
            elif newmode == "scoremode":
                self.mode = Scoremode(done[1],self.screen.get_size(),done[2])
            elif newmode == "clicktocontinue":
                self.mode = ClickToContinue(done[1],
                                            self.screen.get_size(),
                                            done[2])
            elif newmode == "clicktocontinue_scoremode_loss":
                self.mode = ClickToContinue(done[1],
                                            self.screen.get_size(),
                                            done[2],
                                            wait=700)
            elif newmode == "mainmenu":
                self.mode = Mainmenu(self.screen.get_size())
            else:
                print newmode
                print "No matching mode"



if __name__ == "__main__":
    g = Game()
    g.loop()
