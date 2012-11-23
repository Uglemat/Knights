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
