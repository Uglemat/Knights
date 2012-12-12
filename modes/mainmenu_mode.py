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
from knights.menu import Menu
import pygame

class Mainmenu(Menu):
    def __init__(self,screensize):
        self.name = "Mainmenu"

        self.title = MAINMENU['title']

        self.button_info = [{"name": "scoremode",
                             "text": MAINMENU['start-button-text']},

                            {"name": "timesavemode",
                             "text": MAINMENU['timesave-button-text']},

                            {"name": "highscore",
                             "text": MAINMENU['highscore-button-text']},

                            {"name": "help",
                             "text": MAINMENU['help-button-text']},

                            {"name": "exit",
                             "text": MAINMENU['exit-button-text']}]

        super(Mainmenu, self).__init__(screensize)
