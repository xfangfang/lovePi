
import os
from sys import argv


# gui position

HEIGHT = 240
WIDTH = 240
FPS = 24

FONT_SMALL = 0.8
FONT_NORMAL = 1.3
FONT_TITLE = 2.4
FONT_LARGE = 4.8

LINE_1 = 0.9
LINE_2 = 0.8
LINE_3 = 0.7
LINE_4 = 0.6
LINE_5 = 0.5
LINE_6 = 0.4

CENTER = 999

POSITION_SPEEK = (0,0.2)
POSITION_START = (0,0)
POSITION_TALK_FANG = (0,-0.05)
POSITION_TALK_TING = (-0.1,0.05)
SIZE_WINDOW = (1,1)

# const
PI = 1
PC = 2
ENV = PC

# env
script,first = argv
if first == 'PI':
    ENV = PI
    print('ENV: PI')
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
else:
    print('ENV: PC')

# config

confs = os.listdir('conf')
for i in confs:
    f = i.split('.')
    if len(f) == 2 and f[1] == 'yaml':
        locals()['CONF_'+f[0].upper().replace('-','_')] = 'conf/'+i

# font
FONT_FILE_PATH = 'assets/FZMiaoWuJW.TTF'

USERLOG = 'userlog'
IMAGES_ROOT = 'assets/images'

# image
assets = os.listdir('assets')
for i in assets:
    f = i.split('.')
    if len(f) == 2 and ( f[1] == 'png' or f[1] == 'jpg' or f[1] == 'jpeg'):
        locals()[f[0].upper().replace('-','_')] = 'assets/'+i

# color
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
BROWN = (169, 121,  80)
TANTAN_BACKGROUND = (199, 86, 65)
GREY = (128, 128, 128)
PINK = (249, 231, 238)

# activitys state
CATGAME_INIT = 0
CATGAME_START = 1
CATGAME_PAUSE = 2
CATGAME_LOSE = 3
CATGAME_WIN = 4

TAN_START = 0
TAN_SEEK = 1
TAN_CONFIRM = 2

START = 0
SHOW_TIP_ALREADY_UPDATE = 2
SHOW_TIP_REBOOT = 3
SHOW_TIP_NEWGAME = 4
SETTING = 5
UPDATE = 6
IMAGES = 7
ABOUT = 8
RETURN_SETTING = 9


CHOICE_YES = 0
CHOICE_NO = 1
CHOICE_A = 0
CHOICE_B = 1
CHOICE_C = 2

ACTIVITY_START = 0
ANIMATE_START = ACTIVITY_START
ACTIVITY_RUN = 1
ACTIVITY_CLOSE = 2
