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


from knights.settings import MAINMENU
from knights.gui_elements import Textbox, Button
from knights.common import nice_print
import pygame

class Mainmenu(object):
    def __init__(self,screensize):
        self.name = "Mainmenu"

        self.background_color = MAINMENU['bgcolor']
        self.background=pygame.Surface(screensize).convert()
        self.background.fill(self.background_color)
        self.width, self.height = screensize

        self.changed = True

        self.main_text = Textbox(
            name="main_text",
            size=MAINMENU['title-size'],
            location=(0,0),
            text_color=MAINMENU['title-color'],
            surface_color=MAINMENU['title-bgcolor'],
            text_size=MAINMENU['title-text-size'])

        self.main_text.update(MAINMENU['title'])

        button_height = (self.height-MAINMENU['title-size'][1])/5-MAINMENU['button-padding']
        button_size   = (self.width-(MAINMENU['button-padding']*2),button_height)

        self.scoremode_button = Button(
            name="scoremode",
            size=button_size,
            text=MAINMENU['start-button-text'],
            location=(0,0))

        self.timesave_button = Button(
            name="timesavemode",
            size=button_size,
            text=MAINMENU["timesave-button-text"],
            location=(0,0))

        self.highscore_button = Button(
            name="highscore",
            size=button_size,
            text=MAINMENU['highscore-button-text'],
            location=(0,0))

        self.exit_button = Button(
            name="exit",
            size=button_size,
            text=MAINMENU['exit-button-text'],
            location=(0,0))
        
        self.help_button = Button(
            name="help",
            size=button_size,
            text=MAINMENU['help-button-text'],
            location=(0,0))

        calc_button_top = lambda n: (self.height - 
                                     button_height*n - 
                                     MAINMENU['button-padding']*(n-1) - 
                                     MAINMENU['button-padding'])

        self.scoremode_button.rect = self.scoremode_button.surface.get_rect(
            top=calc_button_top(5),
            centerx=self.width/2)
        self.timesave_button.rect = self.timesave_button.surface.get_rect(
            top=calc_button_top(4),
            centerx=self.width/2)
        self.highscore_button.rect = self.highscore_button.surface.get_rect(
            top=calc_button_top(3),
            centerx=self.width/2)
        self.help_button.rect = self.help_button.surface.get_rect(
            top=calc_button_top(2),
            centerx=self.width/2)
        self.exit_button.rect = self.exit_button.surface.get_rect(
            top=calc_button_top(1),
            centerx=self.width/2)

        self.background.blit(
            self.main_text.surface,
            self.main_text.surface.get_rect(
                centery=MAINMENU['title-center-y'],
                centerx=self.width/2
                ))

        self.background.blit(self.scoremode_button.surface,
                             self.scoremode_button.rect)
        self.background.blit(self.timesave_button.surface,
                             self.timesave_button.rect)
        self.background.blit(self.highscore_button.surface,
                             self.highscore_button.rect)
        self.background.blit(self.exit_button.surface,
                             self.exit_button.rect)
        self.background.blit(self.help_button.surface,
                             self.help_button.rect)


        self.buttons = [self.scoremode_button,
                        self.timesave_button,
                        self.highscore_button,
                        self.exit_button,
                        self.help_button]

        self.buttonevents = []


    def update(self):
        self.changed = False
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())
            if button.clicked():
                self.buttonevents.append(button)
            if button.changed:
                nice_print(["Button {0!r} changed:".format(button.name),
                            "Blitting on {0!r}".format(self.name)])
                self.background.blit(button.surface,button.rect)
                self.changed = True
                button.changed = False


    def mousedown(self,pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                nice_print(["Clicked button {0!r}".format(button.name)])
                button.mousedown()
                return

    def mouseup(self,pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.mouseup()
                return

    def button_clicked(self):
        try:
            button = self.buttonevents.pop()
            yield button.name
        except IndexError:
            pass

    def done(self):
        pass
