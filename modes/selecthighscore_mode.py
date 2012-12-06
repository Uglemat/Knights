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
from knights.settings import SELECTHIGHSCORE
from knights.gui_elements import Textbox, Button
from modes.mainmenu_mode import Mainmenu
import pygame

class SelectHighscore(Mainmenu):
    def __init__(self,screensize):
        self.name = "SelectHighscore"
        self.background_color = SELECTHIGHSCORE['bgcolor']
        self.background=pygame.Surface(screensize).convert()
        self.background.fill(self.background_color)
        self.width, self.height = screensize

        self.changed = True

        self.main_text = Textbox(
            name="main_text",
            size=SELECTHIGHSCORE['title-size'],
            location=(0,0),
            text_color=SELECTHIGHSCORE['title-color'],
            surface_color=SELECTHIGHSCORE['title-bgcolor'],
            text_size=SELECTHIGHSCORE['title-text-size'])

        self.main_text.update(SELECTHIGHSCORE['title'])

        button_height = ((self.height-SELECTHIGHSCORE['title-size'][1])/3 - 
                         SELECTHIGHSCORE['button-padding'])
        button_size   = (self.width-(SELECTHIGHSCORE['button-padding']*2),button_height)

        self.normalgame_highscore_button = Button(
            name="normalgame_highscore_button",
            size=button_size,
            text="Normal Highscores",
            location=(0,0))

        self.timesave_highscore_button = Button(
            name="timesave_highscore_button",
            size=button_size,
            text="Timesave Highscores",
            location=(0,0))

        self.back_highscore_button = Button(
            name="back_highscore_button",
            size=button_size,
            text="Back",
            location=(0,0))

        calc_button_top = lambda n: (self.height - 
                                     button_height*n - 
                                     SELECTHIGHSCORE['button-padding']*(n-1) - 
                                     SELECTHIGHSCORE['button-padding'])

        self.normalgame_highscore_button.rect = self.normalgame_highscore_button.surface.get_rect(
            top=calc_button_top(3),
            centerx=self.width/2)
        self.timesave_highscore_button.rect = self.timesave_highscore_button.surface.get_rect(
            top=calc_button_top(2),
            centerx=self.width/2)
        self.back_highscore_button.rect = self.back_highscore_button.surface.get_rect(
            top=calc_button_top(1),
            centerx=self.width/2)

        self.background.blit(
            self.main_text.surface,
            self.main_text.surface.get_rect(
                centery=SELECTHIGHSCORE['title-center-y'],
                centerx=self.width/2
                ))

        self.background.blit(self.normalgame_highscore_button.surface,
                             self.normalgame_highscore_button.rect)
        self.background.blit(self.timesave_highscore_button.surface,
                             self.timesave_highscore_button.rect)
        self.background.blit(self.back_highscore_button.surface,
                             self.back_highscore_button.rect)

        self.buttons = [self.normalgame_highscore_button,
                        self.timesave_highscore_button,
                        self.back_highscore_button]
        self.buttonevents = []
