
import os

# var
HEIGHT = 240
WIDTH = 240
FPS = 60


# const
PI = 1
PC = 2
ENV = PC


if "GAME_DEV" in os.environ and os.environ["GAME_DEV"] == 'PI':
    ENV = PI
    print('ENV: PI')
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
else:
    print('ENV: PC')

CONF_START = 'conf/start.yaml'
CONF_ACTIVITY = 'conf/activity.yaml'
CONF_ANIMATE = 'conf/animate.yaml'
FONT_FILE_PATH = 'assets/FZMiaoWuJW.TTF'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
