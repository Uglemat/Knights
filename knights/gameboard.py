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

import pygame
from knights.gameboard_logic import Gameboard, Field
from knights.settings import BOARD
from knights.settings import PYGAME_FIELD

class PygameField(pygame.sprite.Sprite):
    def __init__(self,field_size,logicfield,field_representation):
        pygame.sprite.Sprite.__init__(self)
        self.logicfield = logicfield

        self.representation = field_representation

        self.changed = True
        self.image = pygame.Surface((field_size,field_size))

        self.error = 0
        self.errorlength = PYGAME_FIELD['error-length']

        self.update()
        self.rect = self.image.get_rect()
        self.clickrect = self.image.get_rect()

    def error_update(self):
        if self.error > 0:
            self.error -= 1
            if self.error == self.errorlength+1 or self.error == 0:
                self.changed = True

    def update(self):
        self.changed = False
        if self.error > 0:
            representation = self.representation["error"]
        else:
            representation = self.representation[self.logicfield.type]

        self.image.blit(representation,(0,0))


class Board(Gameboard):
    def __init__(self,width_height,size,field_offset=5):
        super(Board,self).__init__(size)
        self.pygame_fields = []
        self.wh = width_height
        box_size = (float(self.wh) / self.size)

        field_size = int(box_size-field_offset)-1

        load = lambda name: pygame.image.load(name)

        _open   = load(BOARD['open']).convert()
        knight  = load(BOARD['knight']).convert()
        visited = load(BOARD['visited']).convert()
        block   = load(BOARD['block']).convert()
        error   = load(BOARD['error']).convert()
        base    = load(BOARD['base'])

        img_name = [(_open,"open"),
                    (knight,"knight"),
                    (visited,"visited"),
                    (block,"block"),
                    (error,"error")]

        field_representation = {}
        for image, name in img_name:
            image.blit(base,(0,0))
            image = pygame.transform.scale(image,(field_size,field_size))
            field_representation[name] = image


        for field in self.board:
            coords = ((field.x-1)*box_size+field_offset,(field.y-1)*box_size+field_offset)
            tmpf = PygameField(int(box_size-field_offset),field,field_representation)
            tmpf.rect = tmpf.rect.move(coords[0],coords[1])
            tmpf.clickrect = tmpf.rect.inflate((field_offset+1,field_offset+1))
            self.pygame_fields.append(tmpf)

    def update_fields(self):
        for field in self.pygame_fields:
            field.update()

    def get_current_field(self):
        for field in self.pygame_fields:
            if field.logicfield.get_coords() == self.knight_pos:
                return field
        return False

    def fieldclick(self,coords):
        for field in self.pygame_fields:
            if field.clickrect.collidepoint(coords):
                old_field = self.get_current_field()
                newfield_type = self.move_knight(field.logicfield.get_coords())
                if not newfield_type: # If unvalid move
                    if field.logicfield.type in ["open","visited"]:
                        field.error = field.errorlength
                        field.changed = True
                    return False
                else:    # <- If it's a valid move and knight has moved
                    old_field.changed = True
                    field.changed = True
                    return newfield_type
