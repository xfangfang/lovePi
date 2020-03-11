import time
import sys
import os
import pygame
import random
from pygame.locals import *

from keys import Key

if "GAME_DEV" in os.environ and os.environ["GAME_DEV"] == 'PI':
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
DISPLAYSURF = pygame.display.set_mode((128, 128), 0, 32)

class App():
    def __init__(self):
        pygame.init()
        self.test()

    def test(self):
        # set up the window
        pygame.display.set_caption('LovePi')
        pygame.mouse.set_visible(False)


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
        if e == key.btn_key1:
            list1 = [BLUE, RED, GREEN, BLACK]
            pygame.draw.circle(DISPLAYSURF, random.choice(list1), (40, 50), 20, 0)
            print('click key 1',e)

    def onKeyUp(self, key, e):
        print(e)

def main():
    # main app
    app = App()
    # set Keyboard listener
    key = Key()
    key.setOnKeyUpListener(app.onKeyUp)
    key.setOnKeyDownListener(app.onKeyDown)

    # run the game loop
    while True:
        key.update()
        time.sleep(0.02)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == '__main__':
    main()
