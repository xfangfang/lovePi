
import os
from sys import argv

script,first = argv

# var
HEIGHT = 240
WIDTH = 240
FPS = 24


# const
PI = 1
PC = 2
ENV = PC

os.environ['SDL_NOMOUSE'] = '1'
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

# BACKGROUND_WM = 'assets/background-wm.png'
# PIC_TANTAN = 'assets/tantan.png'
# PIC_SPEEK_LEFT = 'assets/speek_left.png'
# PIC_SPEEK_RIGHT = 'assets/speek_right.png'
# PIC_SPEEK_P_RIGHT = 'assets/speek-p-r.png'
# PIC_SPEEK_B_RIGHT = 'assets/speek-b-r.png'
# PIC_SPEEK_P_LEFT = 'assets/speek-p-l.png'
# PIC_SPEEK_B_LEFT = 'assets/speek-b-l.png'
# PIC_TING_MAD = 'assets/ting-mad.png'
# image
assets = os.listdir('assets')
for i in assets:
    f = i.split('.')
    if len(f) == 2 and f[1] == 'png':
        locals()[f[0].upper().replace('-','_')] = 'assets/'+i

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

LINE_1 = 0.9
LINE_2 = 0.8

CENTER = 999
