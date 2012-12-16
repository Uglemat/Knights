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

from knights.meta import VERSION
from knights.common import settings, settings_regex, setting_changed

if sys.version_info[0] < 3: # Not python 3
    from yaml.lib import yaml
    from yaml.lib.yaml.parser import ParserError
else: # Python 3, or python 4 if you're from the distant future
    from yaml.lib3 import yaml
    from yaml.lib3.yaml.parser import ParserError


"""
 Any command line argument that matches settings_regex, will _not_ be handled with this file,
 they are handled in the function args_overwrite_settings in knights/common.py

 The function is not in this file as to avoid circular dependencies.
"""


def print_setting(n, setting, default):
    print("{indent}{setting:<{width}}VALUE: {def_val}".format(indent=" "*n,
                                                                setting=setting,
                                                                def_val=default,
                                                                width=40-n))

def do_stuff_with_args():
    exit_after = False
    for arg in sys.argv[1:]:
        match = re.match(settings_regex,arg)
        if not match:
            if arg in ["--version","-v"]:
                print("Knights version: {0}".format(VERSION))
                exit_after = True
            elif arg in ["--settings","-s"]:
                for key in settings:
                    val = settings[key]
                    if isinstance(val, dict):
                        print("{0}:".format(key))
                        for subsetting in val:
                            print_setting(4,subsetting,val[subsetting])
                        print("")
                    else:
                        print_setting(0,key,val)
                        print("")
                exit_after = True
            elif arg in ["-help","--help","help","-h","?","--h"]:
                arg_str = lambda s: "{0:<15}".format(s)
                print("Arguments:")
                print(arg_str("--version, -v"), "Print game version")
                print(arg_str("--settings, -s"), "List all possible settings")
                print(arg_str("--help, -s"), "List arguments")
                print(arg_str("setting=value"),"Set some setting to some value. To access nested settings,")
                print(arg_str(""),"use dot notation. value can be enclosed in strings.")
                exit_after = True
            else:
                print("Argument makes non sense: {0}".format(arg))
    if exit_after:
        if not setting_changed:
            exit()
