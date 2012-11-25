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


from settings import TEXTBOX
from settings import BUTTON
from settings import SIDEBAR
from settings import SCOREBOX
from settings import TIMEBOX
from settings import LEVELBOX

from common import nice_print
import pygame

class Sidebar(object):
    def __init__(self,score,sidebar_size,boardsize):
        self.width, self.height = sidebar_size
        self.surface = pygame.Surface(sidebar_size)
        self.bgcolor = SIDEBAR['bgcolor']
        self.left_padding = boardsize + SIDEBAR['board-padding'] 

        self.surface.fill(self.bgcolor)
        self.score = score

        self.changed = True


        btn_margin = SIDEBAR['button-margin']
        btn_width  = self.width - (btn_margin*2)
        btn_height = SIDEBAR['button-height']
        btn_size   = (btn_width,btn_height)

        calc_location = lambda n: (btn_margin,self.height-(btn_height+btn_margin)*n)


        pause_location    = calc_location(4)
        restart_location  = calc_location(3)
        mainmenu_location = calc_location(2)
        quit_location     = calc_location(1)


        self.score_box = Textbox(name = "scorebox",
                                 size =         (self.width,
                                                 SCOREBOX['height']),
                                 location =     SCOREBOX['location'],
                                 text_color =   SCOREBOX['text-color'],
                                 surface_color= SCOREBOX['bgcolor'],
                                 text_size =    SCOREBOX['text-size'])

        self.time_box = Textbox(name="timebox",
                                size =         (self.width,
                                                TIMEBOX['height']),
                                location =     TIMEBOX['location'],
                                text_color =   TIMEBOX['text-color'],
                                surface_color= TIMEBOX['bgcolor'],
                                text_size =    TIMEBOX['text-size'],
                                bold=True)

        self.level_box = Textbox(name="levelbox",
                                 size =         (self.width,
                                                 LEVELBOX['height']),
                                 location =     LEVELBOX['location'],
                                 text_color =   LEVELBOX['text-color'],
                                 surface_color= LEVELBOX['bgcolor'],
                                 text_size =    LEVELBOX['text-size'])


        self.pause    = Button("pause",btn_size,SIDEBAR['pause-text'],pause_location)
        self.restart  = Button("restart",btn_size,SIDEBAR['restart-text'],restart_location)
        self.mainmenu = Button("main_menu",btn_size,SIDEBAR['mainmenu-text'],mainmenu_location)
        self.quit     = Button("quit",btn_size,SIDEBAR['quit-text'],quit_location)

        self.buttons = [self.pause,
                        self.restart,
                        self.mainmenu,
                        self.quit]

        self.buttonevents = []

    def update(self):
        self.changed = False
        for button in self.buttons:
            button.update_hover_status(pygame.mouse.get_pos(),self.left_padding)
            if button.click_animate() == "done":
                self.buttonevents.append(button)
            if button.changed:
                nice_print(["Button {0!r} changed:".format(button.name),
                            "Blitting on sidebar"])

                self.surface.blit(button.surface,button.rect)
                self.changed = True
                button.changed = False

        if self.score_box.changed:
            self.changed = True
            nice_print(["Textbox {0!r} changed:".format(self.score_box.name),
                        "Blitting on sidebar"])
            self.reset()
            self.surface.blit(self.level_box.surface,self.level_box.rect)
            self.surface.blit(self.time_box.surface,self.time_box.rect)
            self.surface.blit(self.score_box.surface,self.score_box.rect)

        if self.time_box.changed:
            self.changed = True
            nice_print(["Textbox {0!r} changed:".format(self.time_box.name),
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

    def mousedown(self,pos):
        for button in self.buttons:
            br = button.rect.move((self.left_padding,0))
            if br.collidepoint(pos):
                nice_print(["Clicked button {0!r}".format(button.text)])
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
        self.color = BUTTON['bgcolor']
        self.clicking_color = BUTTON['clicked_color']
        self.is_hovering = False

        self.clickamount = BUTTON['click-length']
        self.is_clicking = 0

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.rect = self.surface.get_rect()
        self.rect = self.rect.move((location[0],location[1]))

        self.blit_text()

    def blit_text(self):
        font = pygame.font.SysFont(BUTTON['font'],
                                   BUTTON['font-size'],
                                   bold=BUTTON['bold'])
        font = font.render(self.text,1,BUTTON['text-color'])
        renderpos = font.get_rect(centerx=self.width/2,centery=self.height/2)
        self.surface.blit(font,renderpos)

    def update_hover_status(self,pos,left_padding=0):
        br = self.rect.move((left_padding,0))
        if br.collidepoint(pos):
            if not self.is_hovering:
                self.changed = True
                self.is_hovering = True
                self.render_button()
        elif self.is_hovering:
            self.is_hovering = False
            self.changed = True
            self.render_button()

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
        elif self.is_hovering:
            self.surface.fill((111,45,3))
            self.blit_text()
        else:
            self.surface.fill(self.color)
            self.blit_text()

class Textbox(object):
    def __init__(self,name,size,location,text_color,
                 surface_color,text_size,text="",
                 bold=TEXTBOX['default-bold'],
                 font=TEXTBOX['default-font']):
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
