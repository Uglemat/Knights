from settings import HIGHSCORE

from scores import get_highscores
from gui_elements import Textbox

import pygame

class Highscore(object):
    def __init__(self,screensize):
        self.name = "highscore"
        self.hasclicked = False
        self.width = screensize[0]
        self.background = pygame.Surface(screensize).convert()
        self.background.fill(HIGHSCORE['bgcolor'])
        self.changed = True
        highscores = get_highscores(HIGHSCORE['show-n-scores'])

        title = Textbox(
            name="highscore_title",
            size=HIGHSCORE['title-size'],
            location=(0,0),
            text_color=HIGHSCORE['title-text-color'],
            surface_color=HIGHSCORE['title-bgcolor'],
            text_size=HIGHSCORE['title-text-size'],
            bold=HIGHSCORE['title-bold'])
        title.update(HIGHSCORE['title-text'])

        score_boxes = []
        placement = 0

        for i in highscores:
            placement += 1
            highscore = Textbox(
                name="highscore_title",
                size=HIGHSCORE['score-size'],
                location=(0,0),
                text_color=HIGHSCORE['score-text-color'],
                surface_color=HIGHSCORE['score-bgcolor'],
                text_size=HIGHSCORE['score-text-size'],
                bold=HIGHSCORE['score-bold'],
                font=HIGHSCORE['score-font'])
            highscore.update(
                '{:<2}'.format(str(placement))+HIGHSCORE['score-separator']+
                '{:>15}'.format(str(i))
                )

            self.background.blit(highscore.surface,
                                 highscore.surface.get_rect(
                    centery=60+45*placement,
                    centerx=self.width/2
                    ))
            
        self.background.blit(title.surface,
                             title.surface.get_rect(
                centery=50,
                centerx=self.width/2
                ))


    def update(self):
        if self.changed:
            self.changed = False

    def mousedown(self,pos):
        self.hasclicked = True

    def done(self):
        if self.hasclicked:
            return ("mainmenu",'')
        else:
            return False
