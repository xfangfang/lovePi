import time
import sys
import os
import pygame
import random
from pygame.locals import *

from keys import Key
from activity.mainActivity import MainActivity
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
        self.key = Key()
        self.key.setOnKeyUpListener(self.onKeyUp)
        self.key.setOnKeyDownListener(self.onKeyDown)
        self.key.setOnKeyContinueDownListener(self.onKeyContinueDown)
        self.activityStack = []
        self.activityData = {}
        self.background = None

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
        return int(scale * HEIGHT * 1.0 / 16)

    def scaleToWidthPixel(self, scale):
        return int(scale * WIDTH * 1.0 / 16)

    def text(self, text='', size=FONT_NORMAL, position=(0,0), color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.scaleToHeightPixel(size)).render(text, True, color)
        rect = font.get_rect()
        x = position[0]*1.0
        y = position[1]*1.0
        if x < 0:
            # auto center
            w = int((self.WIDTH-rect.right)/2)
        else:
            w = int(self.WIDTH*x)
        if y < 0:
            h = int((self.HEIGHT-rect.bottom)/2)
        else:
            h = int(self.HEIGHT*y)
        self.surf.blit(font,(w,h))

    def update(self):
        if self.background:
            if  isinstance(self.background,tuple):
                self.surface.fill(self.background)
            else:
                back = pygame.image.load(self.background).convert()
                back = pygame.transform.scale(back,(self.WIDTH,self.HEIGHT))
                self.surface.blit(back,(0,0))
        if self.currentActivity:
            self.currentActivity.update()
            self.surface.blit(self.currentActivity.surf, (self.currentActivity.x,self.currentActivity.y))

        self.key.update()

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
        app.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        app.fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
