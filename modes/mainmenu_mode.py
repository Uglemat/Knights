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


from settings import MAINMENU
from gui_elements import Textbox, Button

from common import nice_print
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

        self.scoremode_button = Button(
            name="scoremode",
            size=MAINMENU['start-button-size'],
            text=MAINMENU['start-button-text'],
            location=(0,0))

        self.highscore_button = Button(
            name="highscore",
            size=MAINMENU['highscore-button-size'],
            text=MAINMENU['highscore-button-text'],
            location=(0,0))

        self.exit_button = Button(
            name="exit",
            size=MAINMENU['exit-button-size'],
            text=MAINMENU['exit-button-text'],
            location=(0,0))

        self.scoremode_button.rect = self.scoremode_button.surface.get_rect(
            centery=MAINMENU['start-button-center-y'],
            centerx=self.width/2)

        self.highscore_button.rect = self.highscore_button.surface.get_rect(
            centery=MAINMENU['highscore-button-center-y'],
            centerx=self.width/2)

        self.exit_button.rect = self.exit_button.surface.get_rect(
            centery=MAINMENU['exit-button-center-y'],
            centerx=self.width/2)

        self.background.blit(
            self.main_text.surface,
            self.main_text.surface.get_rect(
                centery=MAINMENU['title-center-y'],
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
            button.update_hover_status(pygame.mouse.get_pos())
            if button.click_animate() == "done":
                self.buttonevents.append(button)
            if button.changed:
                nice_print(["Button {0!r} changed:".format(button.name),
                            "Blitting on main menu"])
                self.background.blit(button.surface,button.rect)
                self.changed = True
                button.changed = False


    def mousedown(self,pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                nice_print(["Clicked button {0!r}".format(button.name)])
                button.is_clicking = button.clickamount

    def button_clicked(self):
        try:
            button = self.buttonevents.pop()
            yield button.name
        except IndexError:
            pass

    def done(self):
        pass
