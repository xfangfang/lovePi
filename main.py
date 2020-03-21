import time
import sys
import os
import pygame
import random
from pygame.locals import *

from keys import Key
from activity.cat import CatGame
from activity.loop import MainActivity
from utils import get_yaml_data
from var import *

class App():
    def __init__(self):
        pygame.init()
        # pygame.display.set_caption('LovePi')
        pygame.mouse.set_visible(False)
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fpsClock = pygame.time.Clock()
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.HEIGHT_SCALE = HEIGHT / 16
        self.WIDTH_SCALE = HEIGHT / 16
        self.key = Key()
        self.key.setOnKeyUpListener(self.onKeyUp)
        self.key.setOnKeyDownListener(self.onKeyDown)
        self.key.setOnKeyContinueDownListener(self.onKeyContinueDown)
        self.activityStack = []

    def currentActivity():
        doc = "The currentActivity property."
        def fget(self):
            nums = len(self.activityStack)
            if nums == 0:
                return None
            else:
                return self.activityStack[nums-1]
        return locals()
    currentActivity = property(**currentActivity())

    def scaleToHeightPixel(self, scale):
        return scale * self.HEIGHT_SCALE

    def scaleToWidthPixel(self, scale):
        return scale * self.WIDTH_SCALE

    def update(self):
        self.key.update()
        if self.currentActivity:
            self.currentActivity.update()
            self.surface.blit(self.currentActivity.surf, (self.currentActivity.x,self.currentActivity.y))

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
        if self.currentActivity:
            self.currentActivity.onKeyDown(key, e)

    def onKeyUp(self, key, e):
        if self.currentActivity:
            self.currentActivity.onKeyUp(key, e)

    def onKeyContinueDown(self, key, e):
        if self.currentActivity:
            self.currentActivity.onKeyContinueDown(key, e)

    def openActivity(self, activityClass):
        activity = activityClass(self)
        self.activityStack.append(activity)

    def close(self):
        if self.currentActivity:
            self.activityStack.pop()

def main():
    # main app
    app = App()
    app.openActivity(MainActivity)

    # run the game loop
    while True:
        app.surface.fill(WHITE)
        app.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        app.fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
