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
from __future__ import print_function
import time
import webbrowser
import os
import sys
import re

if sys.version_info[0] < 3: # Not python 3
    from yaml.lib import yaml
    from yaml.lib.yaml.parser import ParserError
else: # Python 3, or python 4 if you're from the distant future
    from yaml.lib3 import yaml
    from yaml.lib3.yaml.parser import ParserError

subsetting     = '([\w\-]+)\.([\w\-]+)="?(.+)"?'  # Example match: menu.bgcolor="[240,40,100]"
not_subsetting = '([\w\-]+)="?(.+)"?'             # Example match: log-to-console=true
settings_regex = re.compile("{subsetting}|{setting}".format(subsetting=subsetting, 
                                                            setting=not_subsetting))

def args_overwrite_settings(settings):
    setting_changed = False
    for arg in sys.argv[1:]:
        match = re.match(settings_regex,arg)
        if match:
            groups = match.group(1,2,3, 4,5)

            failed_setting = lambda _setting: "\tFAILED! Parsing error: '{0}'".format(_setting)
            non_existent_setting = lambda _setting: "WARNING! No such setting: {0}".format(_setting)

            if groups[0]:      # subsetting matched
                try:
                    settings[groups[0]][groups[1]]
                except KeyError:
                    print(non_existent_setting("{0}.{1}".format(groups[0],group[1])))

                print("Temporarily changing setting {0}.{1}\t-->\t{2}".format(groups[0],groups[1],groups[2]))
                try:
                    settings[groups[0]][groups[1]] = yaml.load(groups[2])
                    setting_changed = True
                except ParserError:
                    print(failed_setting(groups[2]))
            elif groups[3]:     # setting matched
                try:
                    settings[groups[3]]
                except KeyError:
                    print(non_existent_setting(groups[3]))


                print("Temporarily changing setting {0}\t-->\t{1}".format(groups[3],groups[4]))
                try:
                    settings[groups[3]] = yaml.load(groups[4])
                    setting_changed = True
                except ParserError:
                    print(failed_setting(groups[4]))
    return settings, setting_changed


settings_file = open("settings.yaml","r").read()
settings = yaml.load(settings_file)
settings, setting_changed = args_overwrite_settings(settings)

def nice_print(args):
    if not settings['log-to-console']:
        return
    base = time.strftime("%H:%M:%S: ")
    for arg in args:
        base += '{0:<33}'.format(arg)
    print(base)

def open_help_in_browser():
    abs_path = os.path.abspath('.') #Absolute path of current working directory
    filename = os.path.join(abs_path,"help", 'help.html')
    nice_print('Trying to open ' + filename)
    webbrowser.open(filename)

