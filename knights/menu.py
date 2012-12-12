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
from knights.settings import MENU
from knights.gui_elements import Textbox, Button
from knights.common import nice_print
import pygame

class Menu(object):
    def __init__(self,screensize):
        self.button_info.reverse()

        self.background_color = MENU['bgcolor']
        self.background=pygame.Surface(screensize).convert()
        self.background.fill(self.background_color)
        self.width, self.height = screensize
        self.changed = True

        self.button_amount = len(self.button_info)

        self.main_text = Textbox(
            name="main_text",
            size=MENU['title-size'],
            location=(0,0),
            text_color=MENU['title-color'],
            surface_color=MENU['title-bgcolor'],
            text_size=MENU['title-text-size'])

        self.main_text.update(self.title)

        button_height = ((self.height-MENU['title-size'][1])/
                         self.button_amount-MENU['button-padding'])
        button_size   = (self.width-(MENU['button-padding']*2),button_height)

        calc_button_top = lambda n: (self.height - 
                                     button_height*n - 
                                     MENU['button-padding']*(n-1) - 
                                     MENU['button-padding'])

        self.buttons = []
        for n, button in enumerate(self.button_info):
            new_button = Button(
                name=button['name'],
                size=button_size,
                text=button['text'],
                location=(0,0))

            new_button.rect = new_button.surface.get_rect(
                top=calc_button_top(n+1),
                centerx=self.width/2)

            self.buttons.append(new_button)

        self.background.blit(
            self.main_text.surface,
            self.main_text.surface.get_rect(
                centery=MENU['title-center-y'],
                centerx=self.width/2))

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
