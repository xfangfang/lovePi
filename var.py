
import os
from sys import argv

script,first = argv

# var
HEIGHT = 240
WIDTH = 240
FPS = 30


# const
PI = 1
PC = 2
ENV = PC


if first == 'PI':
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

BACKGROUND_WM = 'assets/background.png'
PIC_TANTAN = 'assets/tantan.png'
PIC_SPEEK_LEFT = 'assets/speek_left.png'
PIC_SPEEK_RIGHT = 'assets/speek_right.png'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
BROWN = (169, 121,  80)


CATGAME_INIT = 0
CATGAME_START = 1
CATGAME_PAUSE = 2
CATGAME_LOSE = 3
CATGAME_WIN = 4

CHOICE_YES = 0
CHOICE_NO = 1

ACTIVITY_START = 0
ACTIVITY_RUN = 1
ACTIVITY_CLOSE = 2

FONT_NORMAL = 1.3
FONT_TITLE = 2.4
