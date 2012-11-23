import yaml

settings_file = open("settings.yaml","r").read()
settings = yaml.load(settings_file)

GAME            = settings['game']
FREEMODE        = settings['freemode']
CLICKTOCONTINUE = settings['clickToContinue']
SCOREMODE       = settings['scoremode']
BOARD           = settings['board']
SIDEBAR         = settings['sidebar']
BUTTON          = settings['button']
PYGAME_FIELD    = settings['pygame-field']
GAMEBOARD_LOGIC = settings['gameboard-logic']
SCOREBOX        = settings['scorebox']
TIMEBOX         = settings['timebox']
LEVELBOX        = settings['levelbox']
TEXTBOX         = settings['textbox']
MAINMENU        = settings['mainmenu']
HIGHSCORE       = settings['highscore']
