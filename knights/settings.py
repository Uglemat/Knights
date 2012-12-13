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
import sys
import re

if sys.version_info[0] < 3: # Not python 3
    from yaml.lib import yaml
    from yaml.lib.yaml.parser import ParserError
else: # Python 3, or python 4 if you're from the distant future
    from yaml.lib3 import yaml
    from yaml.lib3.yaml.parser import ParserError

VERSION = "2.7"
settings_file = open("settings.yaml","r").read()
settings = yaml.load(settings_file)


suboption = '([\w\-]+)\.([\w\-]+)="?(.+)"?' # Example match: menu.bgcolor="[240,40,100]"
option    = '([\w\-]+)="?(.+)"?'            # Example match: log-to-console=true
settings_regex     = re.compile("{suboption}|{option}".format(suboption=suboption, option=option))


for arg in sys.argv[1:]:
    match = re.match(settings_regex,arg)
    if match:
        parens = match.group(1,2,3, 4,5)

        failed_option = lambda option: "\tFAILED! Parsing error: '{0}'".format(option)
        non_existent_option = lambda option: "WARNING! No such option: {0}".format(option)

        if parens[0]:      # suboption matched
            try:
                settings[parens[0]][parens[1]]
            except KeyError:
                print(non_existent_option("{0}.{1}".format(parens[0],parens[1])))

            print("Setting option {0}.{1}\t-->\t{2}".format(parens[0],parens[1],parens[2]))
            try:
                settings[parens[0]][parens[1]] = yaml.load(parens[2])
            except ParserError:
                print(failed_option(parens[2]))
        elif parens[3]:    #option matched
            try:
                settings[parens[3]]
            except KeyError:
                print(non_existent_option(parens[3]))


            print("Setting option {0}\t-->\t{1}".format(parens[3],parens[4]))
            try:
                settings[parens[3]] = yaml.load(parens[4])
            except ParserError:
                print(failed_option(parens[4]))
    else:
        print("Unknown option: {0}".format(arg))


GAME            = settings['game']
FREEMODE        = settings['freemode']
CLICKTOCONTINUE = settings['clickToContinue']
SCOREMODE       = settings['scoremode']
TIMESAVEMODE    = settings['timesavemode']
BOARD           = settings['board']
SIDEBAR         = settings['sidebar']
BUTTON          = settings['button']
PYGAME_FIELD    = settings['pygame-field']
GAMEBOARD_LOGIC = settings['gameboard-logic']
SCOREBOX        = settings['scorebox']
TIMEBOX         = settings['timebox']
LEVELBOX        = settings['levelbox']
TEXTBOX         = settings['textbox']
MENU            = settings['menu']
MAINMENU        = settings['mainmenu']
SELECTHIGHSCORE = settings['selecthighscore']
HIGHSCORE       = settings['highscore']
