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
import os
import sys

if sys.version_info[0] < 3:
    from yaml.lib import yaml
else:
    from yaml.lib3 import yaml



highscores_file = ".highscores.yaml"

def submit_score(score, gametype="normal-game"):
    if os.path.exists(highscores_file):
        f = open(highscores_file,"r")
        highscores = f.read()
        highscores = yaml.load(highscores)
        f.close()
    else:
        highscores = {gametype:[]}
    with open(highscores_file,"w") as hs:
        try:
            highscores[gametype].append(score)
        except KeyError:
            highscores[gametype] = [score]
        hs.write(yaml.dump(highscores))

def get_highscores(n,gametype="normal-game"):
    if not os.path.exists(highscores_file):
        return []
    with open(highscores_file,"r") as hs:
        try:
            highscores = yaml.load(hs.read())[gametype]
        except KeyError:
            return []
        highscores.sort(reverse=True)

        return highscores[0:n]
