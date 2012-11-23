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
import yaml


highscores_file = ".highscores.yaml"

def submit_score(score):
    if os.path.exists(highscores_file):
        f = open(highscores_file,"r")
        highscores = f.read()
        highscores = yaml.load(highscores)
        f.close()
    else:
        highscores = {'highscores':[]}
    with open(highscores_file,"w") as hs:
        highscores['highscores'].append(score)
        hs.write(yaml.dump(highscores))

def get_highscores(n):
    if not os.path.exists(highscores_file):
        return []
    with open(highscores_file,"r") as hs:
        highscores = yaml.load(hs.read())['highscores']
        highscores.sort(reverse=True)

        return highscores[0:n]
