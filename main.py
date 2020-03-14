import time
import sys
import os
import pygame
import random
from pygame.locals import *

from var import *
from keys import Key
from activity.cat import CatGame
from utils import get_yaml_data

ENV = PC
HEIGHT = 128
WIDTH = 128

# HEIGHT = 240
# WIDTH = 240
if "GAME_DEV" in os.environ and os.environ["GAME_DEV"] == 'PI':
    ENV = PI
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'

# set up the colors

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
fpsClock = pygame.time.Clock()

class App():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('LovePi')
        pygame.mouse.set_visible(False)
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.HEIGHT_SCALE = HEIGHT / 16
        self.WIDTH_SCALE = HEIGHT / 16
        self.key = Key(ENV)
        self.key.setOnKeyUpListener(self.onKeyUp)
        self.key.setOnKeyDownListener(self.onKeyDown)
        self.key.setOnKeyContinueDownListener(self.onKeyContinueDown)

    def scaleToHeightPixel(self, scale):
        return scale * self.HEIGHT_SCALE

    def scaleToWidthPixel(self, scale):
        return scale * self.WIDTH_SCALE

    def update(self):
        self.key.update()

        if self.activity:
            self.activity.update()
    def test(self):
        # draw on the surface object
        DISPLAYSURF.fill(WHITE)
        pygame.draw.polygon(DISPLAYSURF, GREEN, ((16, 0), (36, 0), (56, 27), (0, 106)))
        pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
        pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
        pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
        pygame.draw.circle(DISPLAYSURF, BLUE, (40, 50), 20, 0)
        pygame.draw.ellipse(DISPLAYSURF, RED, (50, 50, 40, 80), 1)
        pygame.draw.rect(DISPLAYSURF, RED, (100, 100, 100, 50))

    def onKeyDown(self, key, e):
        if self.activity:
            self.activity.onKeyDown(key, e)
        # if e == key.btn_key1:
        #     list1 = [BLUE, RED, GREEN, BLACK]
        #     pygame.draw.circle(DISPLAYSURF, random.choice(list1), (40, 50), 20, 0)
        #     print('click key 1',e)

    def onKeyUp(self, key, e):
        if self.activity:
            self.activity.onKeyUp(key, e)

    def onKeyContinueDown(self, key, e):
        if self.activity:
            self.activity.onKeyContinueDown(key, e)

    def setActivity(self, activity):
        self.activity = activity

def main():
    # main app
    app = App()
    catgame = CatGame(app)
    app.setActivity(catgame)
    # set Keyboard listener


    # run the game loop
    while True:
        DISPLAYSURF.fill(WHITE)
        app.update()
        DISPLAYSURF.blit(app.activity.surf, (app.activity.x,app.activity.y))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        fpsClock.tick(60)

if __name__ == '__main__':
    main()
