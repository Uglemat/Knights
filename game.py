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
import time

from pygame.locals import *
from gameboard_logic import Gameboard, Field
from gameboard import PygameField, Board

from settings import settings
from settings import clickToContinue_settings
from settings import sidebar_settings
from settings import button_settings
from settings import scoremode_settings
from settings import freemode_settings
from settings import game_settings
from settings import scorebox_settings
from settings import timebox_settings
from settings import levelbox_settings
from settings import mainmenu_settings
from settings import textbox_settings
from settings import highscore_settings

from scores import submit_score
from scores import top as get_highscores

def nice_print(args):
    if not settings['log-to-console']:
        return
    base = time.strftime("%H:%M:%S: ")
    for arg in args:
        base += '{:<33}'.format(arg)
    print base

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode(game_settings['resolution'])
        pygame.display.set_caption(game_settings['caption'])
        self.clock = pygame.time.Clock()
        self.timeinterval = game_settings['fps-limit']

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
            if i.type==QUIT or i.type==KEYDOWN and i.key==K_ESCAPE:
                exit()
            if i.type==MOUSEBUTTONDOWN:
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

class Mainmenu(object):
    def __init__(self,screensize):
        self.name = "Mainmenu"

        self.background_color = mainmenu_settings['bgcolor']
        self.background=pygame.Surface(screensize).convert()
        self.background.fill(self.background_color)
        self.width, self.height = screensize

        self.changed = True

        self.main_text = Textbox(
            name="main_text",
            size=mainmenu_settings['title-size'],
            location=(0,0),
            text_color=mainmenu_settings['title-color'],
            surface_color=mainmenu_settings['title-bgcolor'],
            text_size=mainmenu_settings['title-text-size'])

        self.main_text.update(mainmenu_settings['title'])

        self.scoremode_button = Button(
            name="scoremode",
            size=mainmenu_settings['start-button-size'],
            text=mainmenu_settings['start-button-text'],
            location=(0,0))

        self.highscore_button = Button(
            name="highscore",
            size=mainmenu_settings['highscore-button-size'],
            text=mainmenu_settings['highscore-button-text'],
            location=(0,0))

        self.exit_button = Button(
            name="exit",
            size=mainmenu_settings['exit-button-size'],
            text=mainmenu_settings['exit-button-text'],
            location=(0,0))

        self.scoremode_button.rect = self.scoremode_button.surface.get_rect(
            centery=mainmenu_settings['start-button-center-y'],
            centerx=self.width/2)

        self.highscore_button.rect = self.highscore_button.surface.get_rect(
            centery=mainmenu_settings['highscore-button-center-y'],
            centerx=self.width/2)

        self.exit_button.rect = self.exit_button.surface.get_rect(
            centery=mainmenu_settings['exit-button-center-y'],
            centerx=self.width/2)

        self.background.blit(
            self.main_text.surface,
            self.main_text.surface.get_rect(
                centery=mainmenu_settings['title-center-y'],
                centerx=self.width/2
                ))

        self.background.blit(self.scoremode_button.surface,
                             self.scoremode_button.rect)

        self.background.blit(self.highscore_button.surface,
                             self.highscore_button.rect)

        self.background.blit(self.exit_button.surface,
                             self.exit_button.rect)


        self.buttons = [self.scoremode_button,
                        self.highscore_button,
                        self.exit_button]

        self.buttonevents = []


    def update(self):
        self.changed = False
        for button in self.buttons:
            if button.click_animate() == "done":
                self.buttonevents.append(button)
            if button.changed:
                nice_print(["Button {!r} changed:".format(button.name),
                            "Blitting on main menu"])
                self.background.blit(button.surface,button.rect)
                self.changed = True
                button.changed = False


    def mousedown(self,pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                nice_print(["Clicked button {!r}".format(button.name)])
                button.is_clicking = button.clickamount

    def button_clicked(self):
        try:
            button = self.buttonevents.pop()
            yield button.name
        except IndexError:
            pass

    def done(self):
        pass

class Freemode(object):
    def __init__(self,level,screensize):
        self.name = "Freemode"
        self.boardsize = screensize[1]-5
        self.level = level

        self.background_color = freemode_settings['bgcolor']
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

class Highscore(object):
    def __init__(self,screensize):
        self.name = "highscore"
        self.hasclicked = False
        self.width = screensize[0]
        self.background = pygame.Surface(screensize).convert()
        self.background.fill(highscore_settings['bgcolor'])
        self.changed = True
        highscores = get_highscores(highscore_settings['show-n-scores'])

        title = Textbox(
            name="highscore_title",
            size=highscore_settings['title-size'],
            location=(0,0),
            text_color=highscore_settings['title-text-color'],
            surface_color=highscore_settings['title-bgcolor'],
            text_size=highscore_settings['title-text-size'],
            bold=highscore_settings['title-bold'])
        title.update(highscore_settings['title-text'])

        score_boxes = []
        placement = 0

        for i in highscores:
            placement += 1
            highscore = Textbox(
                name="highscore_title",
                size=highscore_settings['score-size'],
                location=(0,0),
                text_color=highscore_settings['score-text-color'],
                surface_color=highscore_settings['score-bgcolor'],
                text_size=highscore_settings['score-text-size'],
                bold=highscore_settings['score-bold'],
                font=highscore_settings['score-font'])
            highscore.update(
                '{:<2}'.format(str(placement))+highscore_settings['score-separator']+
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

class ClickToContinue(object):
    def __init__(self,donetuple,screensize,message=False,
                 text_size=clickToContinue_settings['font-size'],wait=0):
        self.name = "ClickToContinue"
        self.donetuple = donetuple
        self.hasclicked = False
        self.background = pygame.Surface(screensize).convert()
        self.background.set_alpha(clickToContinue_settings['alpha'])
        self.background.fill(clickToContinue_settings['bgcolor'])
        self.changed = True
        self.wait_time = wait
        self.clock = pygame.time.Clock()


        if message:
            font = pygame.font.SysFont(clickToContinue_settings['font'],
                                       text_size,
                                       bold=clickToContinue_settings['bold'])
            font = font.render(message,1,clickToContinue_settings['text-color'])
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

class Scoremode(Freemode):
    def __init__(self,level,screensize,score=0):
        super(Scoremode,self).__init__(level,screensize)
        self.name = "Scoremode"
        self.score = score
        self.base_score = scoremode_settings['base-score']
        self.clock = pygame.time.Clock()
        self.timeleft = (51-(5*(level/3)))*1000

        self.level = level


        sidebar_size = (screensize[0]-self.boardsize-sidebar_settings['board-padding'],screensize[1])
        self.sidebar = Sidebar(self.score,sidebar_size)
        self.sidebar_rect = self.sidebar.surface.get_rect()
        self.sidebar_rect = self.sidebar_rect.move((self.boardsize+sidebar_settings['board-padding'],0))

        self.pause = False
        self.pause_color = scoremode_settings['pause-color']
        self.pause_alpha = scoremode_settings['pause-alpha']
        self.pause_text =  scoremode_settings['pause-text']

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

class Sidebar(object):
    def __init__(self,score,sidebar_size):
        self.width, self.height = sidebar_size
        self.surface = pygame.Surface(sidebar_size)
        self.bgcolor = sidebar_settings['bgcolor']

        self.surface.fill(self.bgcolor)
        self.score = score

        self.changed = True

        btn_margin = sidebar_settings['button-margin']
        btn_width  = self.width - (btn_margin*2)
        btn_height = sidebar_settings['button-height']
        btn_size   = (btn_width,btn_height)

        calc_location = lambda n: (btn_margin,self.height-(btn_height+btn_margin)*n)


        pause_location    = calc_location(4)
        restart_location  = calc_location(3)
        mainmenu_location = calc_location(2)
        quit_location     = calc_location(1)


        self.score_box = Textbox(name = "scorebox",
                                 size =         (self.width,
                                                 scorebox_settings['height']),
                                 location =     scorebox_settings['location'],
                                 text_color =   scorebox_settings['text-color'],
                                 surface_color= scorebox_settings['bgcolor'],
                                 text_size =    scorebox_settings['text-size'])

        self.time_box = Textbox(name="timebox",
                                size =         (self.width,
                                                timebox_settings['height']),
                                location =     timebox_settings['location'],
                                text_color =   timebox_settings['text-color'],
                                surface_color= timebox_settings['bgcolor'],
                                text_size =    timebox_settings['text-size'],
                                bold=True)

        self.level_box = Textbox(name="levelbox",
                                 size =         (self.width,
                                                 levelbox_settings['height']),
                                 location =     levelbox_settings['location'],
                                 text_color =   levelbox_settings['text-color'],
                                 surface_color= levelbox_settings['bgcolor'],
                                 text_size =    levelbox_settings['text-size'])


        self.pause    = Button("pause",btn_size,sidebar_settings['pause-text'],pause_location)
        self.restart  = Button("restart",btn_size,sidebar_settings['restart-text'],restart_location)
        self.mainmenu = Button("main_menu",btn_size,sidebar_settings['mainmenu-text'],mainmenu_location)
        self.quit     = Button("quit",btn_size,sidebar_settings['quit-text'],quit_location)

        self.buttons = [self.pause,
                        self.restart,
                        self.mainmenu,
                        self.quit]

        self.buttonevents = []

    def update(self):
        self.changed = False
        for button in self.buttons:
            if button.click_animate() == "done":
                self.buttonevents.append(button)
            if button.changed:
                nice_print(["Button {!r} changed:".format(button.name),
                            "Blitting on sidebar"])

                self.surface.blit(button.surface,button.rect)
                self.changed = True
                button.changed = False

        if self.score_box.changed:
            self.changed = True
            nice_print(["Textbox {!r} changed:".format(self.score_box.name),
                        "Blitting on sidebar"])
            self.reset()
            self.surface.blit(self.level_box.surface,self.level_box.rect)
            self.surface.blit(self.time_box.surface,self.time_box.rect)
            self.surface.blit(self.score_box.surface,self.score_box.rect)

        if self.time_box.changed:
            self.changed = True
            nice_print(["Textbox {!r} changed:".format(self.time_box.name),
                        "Blitting on sidebar"])
            self.reset()
            self.surface.blit(self.level_box.surface,self.level_box.rect)
            self.surface.blit(self.score_box.surface,self.score_box.rect)
            self.surface.blit(self.time_box.surface,self.time_box.rect)
            

    def reset(self):
        self.surface.fill(self.bgcolor)
        for button in self.buttons:
            self.surface.blit(button.surface,button.rect)
            button.changed = True
        self.score_box.blit_text()
        self.changed = True

    def mousedown(self,pos,boardsize):
        for button in self.buttons:
            br = button.rect.move((boardsize+sidebar_settings['board-padding'],0))
            if br.collidepoint(pos):
                nice_print(["Clicked button {!r}".format(button.text)])
                button.is_clicking = button.clickamount

    def button_clicked(self):
        try:
            button = self.buttonevents.pop()
            yield button.name
        except IndexError:
            pass


class Button(object):
    def __init__(self,name,size,text,location):
        self.name = name
        self.changed = True
        self.size = size
        self.width, self.height = self.size
        self.text = text
        self.color = button_settings['bgcolor']
        self.clicking_color = button_settings['clicked_color']

        self.clickamount = button_settings['click-length']
        self.is_clicking = 0

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.rect = self.surface.get_rect()
        self.rect = self.rect.move((location[0],location[1]))

        self.blit_text()

    def blit_text(self):
        font = pygame.font.SysFont(button_settings['font'],
                                   button_settings['font-size'],
                                   bold=button_settings['bold'])
        font = font.render(self.text,1,button_settings['text-color'])
        renderpos = font.get_rect(centerx=self.width/2,centery=self.height/2)
        self.surface.blit(font,renderpos)

    def click_animate(self):
        if self.is_clicking:
            self.is_clicking -= 1
            if self.is_clicking+1 == self.clickamount or self.is_clicking == 0:
                self.changed = True
                self.render_button()
            if self.is_clicking == 0:
                return "done"

    def render_button(self):
        if self.is_clicking:
            self.surface.fill(self.clicking_color)
            self.blit_text()
        else:
            self.surface.fill(self.color)
            self.blit_text()

class Textbox(object):
    def __init__(self,name,size,location,text_color,
                 surface_color,text_size,text="",
                 bold=textbox_settings['default-bold'],
                 font=textbox_settings['default-font']):
        self.name = name
        self.changed = True
        self.size = size
        self.width, self.height = self.size
        self.text_color = text_color
        self.text = text
        self.text_size = text_size
        self.bold = bold
        self.font = font

        self.surface_color = surface_color
        self.surface = pygame.Surface(self.size,pygame.SRCALPHA)
        self.surface.fill(self.surface_color)

        self.rect = self.surface.get_rect()
        self.rect = self.rect.move((location[0],location[1]))

        self.update(text)

    def reset(self):
        self.surface = pygame.Surface(self.size,pygame.SRCALPHA)
        self.surface.fill(self.surface_color)

    def blit_text(self):
        self.reset()
        self.changed = True
        font = pygame.font.SysFont(self.font,
                                   self.text_size,
                                   bold=self.bold)
        font = font.render(self.text,1,self.text_color)

        renderpos = font.get_rect(centerx=self.width/2,centery=self.height/2)
        self.surface.blit(font,renderpos)

    def update(self,text):
        self.changed = False
        if text != self.text:
            self.changed = True
            self.text = text
            self.blit_text()

if __name__ == "__main__":
    g = Game()
    g.loop()
