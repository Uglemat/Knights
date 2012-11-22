import yaml

settings_file = open("settings.yaml","r").read()
settings = yaml.load(settings_file)

game_settings            = settings['game']
freemode_settings        = settings['freemode']
clickToContinue_settings = settings['clickToContinue']
scoremode_settings       = settings['scoremode']
board_settings           = settings['board']
sidebar_settings         = settings['sidebar']
button_settings          = settings['button']
pygame_field_settings    = settings['pygame-field']
gameboard_logic_settings = settings['gameboard-logic']
scorebox_settings        = settings['scorebox']
timebox_settings         = settings['timebox']
levelbox_settings        = settings['levelbox']
mainmenu_settings        = settings['mainmenu']
textbox_settings         = settings['textbox']
highscore_settings       = settings['highscore']
