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
from knights.settings import CLICKTOCONTINUE
import pygame
import time

def render_texts(screensize,texts,f,bold=False,padding=20):
    """Function that generates a surface and a rect out of a list of tuples,
    it renders the text in the center of the surface.
    """
    total_height = 0
    fonts = []
    for text in texts:
        size = text[0]
        color= text[1]
        message = text[2]
        font = pygame.font.SysFont(f,size,bold=bold)
        surf = font.render(message,1,color)
        surf_height = surf.get_rect().height+20
        total_height += surf_height
        fonts.append((surf_height,surf))

    base_surf = pygame.Surface((screensize[0],total_height))
    base_surf.fill((20,20,20))
    base_surf_rect = base_surf.get_rect(centerx=screensize[0]/2,
                                        centery=screensize[1]/2)
    centerx = screensize[0]/2
    placement = 0
    for font in fonts:
        h, s = font
        base_surf.blit(s,s.get_rect(centerx=centerx,top=placement))
        placement += h

    return (base_surf,base_surf_rect)

class ClickToContinue(object):
    def __init__(self,donetuple,screensize,messages=False,wait=0):
        self.name = "ClickToContinue"
        self.donetuple = donetuple
        self.hasclicked = False
        self.background = pygame.Surface(screensize).convert()
        self.background.set_alpha(CLICKTOCONTINUE['alpha'])
        self.background.fill(CLICKTOCONTINUE['bgcolor'])
        self.changed = True
        self.wait_time = wait
        self.clock = pygame.time.Clock()

        if messages:
            text, rect = render_texts(screensize,messages,CLICKTOCONTINUE['font'],
                                      bold=CLICKTOCONTINUE['bold'])
            self.background.blit(text,rect)



    def update(self):
        if self.changed:

            self.changed = False

    def mousedown(self,pos):
        if self.clock.tick() > self.wait_time:
            self.hasclicked = True

    def mouseup(self,pos):
        pass

    def done(self):
        if self.hasclicked:
            return self.donetuple
        else:
            return False
