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

from settings import CLICKTOCONTINUE
import pygame

class ClickToContinue(object):
    def __init__(self,donetuple,screensize,message=False,
                 text_size=CLICKTOCONTINUE['font-size'],wait=0):
        self.name = "ClickToContinue"
        self.donetuple = donetuple
        self.hasclicked = False
        self.background = pygame.Surface(screensize).convert()
        self.background.set_alpha(CLICKTOCONTINUE['alpha'])
        self.background.fill(CLICKTOCONTINUE['bgcolor'])
        self.changed = True
        self.wait_time = wait
        self.clock = pygame.time.Clock()


        if message:
            font = pygame.font.SysFont(CLICKTOCONTINUE['font'],
                                       text_size,
                                       bold=CLICKTOCONTINUE['bold'])
            font = font.render(message,1,CLICKTOCONTINUE['text-color'])
            renderpos = font.get_rect(centerx=screensize[0]/2,centery=screensize[1]/2)
            self.background.blit(font,renderpos)



    def update(self):
        if self.changed:

            self.changed = False

    def mousedown(self,pos):
        if self.clock.tick() > self.wait_time:
            self.hasclicked = True

    def done(self):
        if self.hasclicked:
            return self.donetuple
        else:
            return False
