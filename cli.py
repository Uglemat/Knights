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


from gameboard_logic import Gameboard

def game(): 
    """Sloppy textual version of the game, used in early development.
       You play with the arrow keys, the long move first, the short move second. Then enter."""
    size = raw_input("What size..")
    if size == '': exit()
    gameboard = Gameboard(int(size))

    play_d = {"\x1b[B\x1b[D":(-1,2),
              "\x1b[B\x1b[C":(1,2),
              "\x1b[A\x1b[D":(-1,-2),
              "\x1b[A\x1b[C":(1,-2),
              "\x1b[C\x1b[A":(2,-1),
              "\x1b[C\x1b[B":(2,1),
              "\x1b[D\x1b[A":(-2,-1),
              "\x1b[D\x1b[B":(-2,1),
              "ng":"ng"}
    # Those are just escape sequences for the arrow keys in the terminal or
    # something stupid like that, I don't even care I just copy-pasted. I mean
    # why should I care, we're all gonna die and then it doesn't matter.
    # Aliens won't care a byte. Not even a bit.
    #  Prefix = \x1b[
    #  A = Up
    #  B = Down
    #  C = Right
    #  D = Left


    while 1:
        print "\n" * 50
        gameboard.print_board()

        if gameboard.game_over():
            print "Congratulations, you won!\n"
            game()

        try:
            new_move = play_d[raw_input()]
        except KeyError:
            new_move = (-1000,-1000)
        if new_move == "ng":
            game()
        k_x, k_y = gameboard.knight_pos
        new_move = (k_x + new_move[0],k_y + new_move[1])
        gameboard.move_knight(new_move)

if __name__ == "__main__":
    game()
