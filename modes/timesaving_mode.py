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
from modes.score_mode import Scoremode

from knights.settings import TIMESAVEMODE
from knights.scores import get_highscores, submit_score
from knights.common import nice_print
import pygame

class Timemode(Scoremode):
    def __init__(self,level,screensize,score=0,timeleft=TIMESAVEMODE['level-time']+.99):
        super(Timemode,self).__init__(level,screensize)
        self.name = "Timemode"
        self.timeleft = timeleft*1000
        self.score = score

    def done(self):
        if self.board.game_over():
            timebonus = ((self.timeleft)*(self.level*self.level)*self.base_score)/20/1000

            next_round_time= self.timeleft/1000+TIMESAVEMODE['level-time']+.99
            next_round = ("timesavemode",self.level+1,self.score+timebonus,next_round_time)

            close_call = {True: "   (good luck..)", False: ""}[self.timeleft < 2000]
            messages = [
                (25,TIMESAVEMODE['message-color'],"Level score: " + str(int(self.score-self.prev_score))),
                (25,TIMESAVEMODE['message-color'],"Time saved for next round: " + "{0:.1f}".format(self.timeleft/1000) + " seconds"+close_call),
                (25,TIMESAVEMODE['message-color'],"Timebonus: " + str(int(timebonus))),
                (45,TIMESAVEMODE['message-important-color'],"Total time next round: " + "{0:.1f}".format(next_round_time)),
                (45,TIMESAVEMODE['message-important-color'],"Total score: " + str(int(self.score+timebonus))),
                (20,TIMESAVEMODE['message-color'],"Click to continue to level {0}...".format(self.level+1))]

            return ("clicktocontinue",next_round,messages)
        elif self.timeleft < 100:
            hs = get_highscores(10,"timesave-game")
            if not hs:
                max_hs = 0
                min_hs = 0
            else:
                max_hs = max(hs)
                min_hs = min(hs)

            if self.score > max_hs:
                highscore_message = (30,TIMESAVEMODE['message-important-color'],"Congratulations! You broke the #1 highscore!")
            elif self.score > min_hs or len(hs) < 10:
                highscore_message = (30,TIMESAVEMODE['message-color'],"Your score is in the top 10 highscores!")
            else:
                highscore_message = (30,TIMESAVEMODE['message-color'],"You didn't get on the top 10 highscores.")

            nice_print(["Writing score to file..."])
            submit_score(int(self.score),"timesave-game")
            next_round = ("timesavemode",1,0,TIMESAVEMODE['level-time']+.99)
            messages = [(30,TIMESAVEMODE['message-color'],"Game over!"),
                        (40,TIMESAVEMODE['message-important-color'],"Final score: " + str(int(self.score))),
                        highscore_message,
                        (20,TIMESAVEMODE['message-color'],"Click to start new game...")]

            return ("clicktocontinue_scoremode_loss",next_round,messages)
        else:
            return False
