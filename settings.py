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


import yaml



settings_file = open("settings.yaml","r").read()
settings = yaml.load(settings_file)

game_settings            = settings['game']
freemode_settings        = settings['freemode']
clickToContinue_settings = settings['clickToContinue']
scoremode_settings       = settings['scoremode']
board_settings           = settings['board']
sidebar_settings         = settings['sidebar']
button_settings          = settings['button']
pygame_field_settings    = settings['pygame-field']
gameboard_logic_settings = settings['gameboard-logic']
scorebox_settings        = settings['scorebox']
timebox_settings         = settings['timebox']
levelbox_settings        = settings['levelbox']
mainmenu_settings        = settings['mainmenu']
textbox_settings         = settings['textbox']
highscore_settings       = settings['highscore']
