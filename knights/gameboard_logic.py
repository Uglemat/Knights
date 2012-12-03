# -*- Encoding: utf-8 -*-
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

import random
import sys
sys.setrecursionlimit(2500) # Will allow generate_board to create much larger maps.

from knights.settings import GAMEBOARD_LOGIC

def square(x): return x*x

def concat(l): # Turns [[1],[2],[3]] into [1,2,3]
    newL = []
    for i in l:
        for d in i:
            newL.append(d)
    return newL

def next_step(size,start):
    x, y = start
    possible = [(x-2,y-1),(x-2,y+1),
                (x+2,y-1),(x+2,y+1),
                (x-1,y+2),(x-1,y-2),
                (x+1,y+2),(x+1,y-2)]
    possible = filter(lambda f: f[0] in range(1,size+1) and f[1] in range(1,size+1),possible) # Only coords within game border
    return list(possible)

def generate_board(size,here=(1,1),visited=None,threshold=40):
    """Generate a list of random coordinates that can all be visited by a knight, starting at here"""
    if visited == None:
        visited = []
    if here not in visited:
        visited.append(here)
    if float(len(visited)) / square(size) * 100 > threshold:  # If the percentage of visited fields on the board is greater than the threshold percentage
        return visited

    next_here = random.choice(next_step(size,here)) # Chose a random coord amongst the set of valid next coords
    return generate_board(size,next_here,visited,threshold)


class Field(object):   
    def __init__(self,field_type,coords):
        possible_types = ["knight","visited","block","open"]
        """  knight  : Knight is currently in this field
             visited : Knight has been here
             block   : Knight cannot visit this field
             open    : Knight has not been here yet       """

        self.type = field_type
        self.x, self.y = coords
        self.char_representation = {"visited" : '--',
                                    "knight"  : 'KK',
                                    "block"   : '██',
                                    "open"    : '░░'}

    def get_coords(self):
        return self.x, self.y

    def set_type(self,field_type):
        self.type = field_type

    def as_character(self):
        return self.char_representation[self.type]

class Gameboard(object):
    def __init__(self,size):
        self.size = size
        self.knight_pos = tuple(GAMEBOARD_LOGIC['starting-position'])
        self.populate_board(size)

    def populate_board(self,size):
        self.board = []
        board = concat([[(x,y) for x in range(1,size+1)] for y in range(1,size+1)])
        open_fields = generate_board(size,
                                     self.knight_pos,
                                     threshold=GAMEBOARD_LOGIC['block-percentage'])

        for coords in board:
            field_type = ""
            if coords == self.knight_pos:
                field_type = "knight"
            elif coords in open_fields:
                field_type = "open"
            else:
                field_type = "block"
            self.board.append(Field(field_type,coords))

    def move_knight(self,new_coords):
        possible_moves = next_step(self.size,self.knight_pos)

        open_or_visited = lambda m: self.get_field(m).type in ["open","visited"]

        valid_moves = [m for m in possible_moves if open_or_visited(m)]
        if new_coords in valid_moves:
            newfield = self.get_field(new_coords)
            newfield_type = newfield.type

            self.get_field(self.knight_pos).type = "visited"
            newfield.type = "knight"
            self.knight_pos = new_coords
            return newfield_type
        else:
            return False

    def get_field(self,coords):
        for field in self.board:
            if field.get_coords() == coords:
                return field
        return "No such field!"


    def print_board(self):
        for i in range(1,self.size+1):
            horizontal = ""
            ifields = []
            for field in self.board:
                if field.y == i:
                    ifields.append(field)
            ifields = sorted(ifields,key=lambda f: f.x)
            for field in ifields:
                horizontal += field.as_character()
            print(horizontal)

    def game_over(self):
        for field in self.board:
            if field.type == "open":
                return False
        return True
