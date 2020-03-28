import time
import sys
import os
import pygame
import random
from pygame.locals import *

from keys import Key
from activity.mainActivity import StartActivity
from activity.mainActivity import Text
from activity.mainActivity import Choice
from activity.cat import CatGame

from utils import get_yaml_data
from var import *

pygame.display.init()

class App():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('LovePi')
        pygame.mouse.set_visible(False)
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.surface.fill(WHITE)
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

        # game state
        self.gameloop = get_yaml_data(CONF_START)['gameloop']
        self.buildTag()
        self.gameState = 0

        self.stateChange()

    def buildTag(self):
        self.tagMap = {}
        for i, state in enumerate(self.gameloop):
            if 'tag' in state:
                self.tagMap[state['tag']] = i

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

    def stateChange(self):
        if self.gameState >= len(self.gameloop):
            self.gameState = 0
        state = self.gameloop[self.gameState]
        self.activityData['state'] = state
        if 'background' in state:
            self.background = eval(state['background'])
        if state['type'] == 'activity':
            self.openActivity(eval(state['activity']))
            self.gameState += 1
        elif state['type'] == 'goto':
            if 'status' in self.activityData:
                if self.activityData['status'] == eval(state['if']):
                    if 'goto' in state:
                        self.gameState = int(state['goto'])
                    elif 'goto_tag' in state:
                        self.gameState = self.tagMap[state['goto_tag']]
                    elif 'step' in state:
                        self.gameState += int(state['step'])
                else:
                    self.gameState += 1
            else:
                self.gameState -= 1
            self.stateChange()

    def update(self):
        if self.background != None:
            if isinstance(self.background,tuple):
                self.surface.fill(self.background)
            else:
                back = pygame.image.load(self.background).convert()
                back = pygame.transform.scale(back,(self.WIDTH,self.HEIGHT))
                self.surface.blit(back,(0,0))
        # single activity active
        if self.currentActivity:
            current = self.currentActivity
            current.update()
            self.surface.blit(current.surf, (current.x,current.y))

        # muti activity active
        # for a in self.activityStack:
        #     a.update()
        #     self.surface.blit(a.surf, (a.x,a.y))

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
            self.stateChange()

    def updateAndRestart(self):
        os.system("git pull")
        python = sys.executable
        os.execl(python, python, * sys.argv)

def main():
    # main app
    app = App()
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
