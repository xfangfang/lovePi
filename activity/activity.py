import pygame
import math
from var import *
from animate import *

class Activity():
    def __init__(self, app):
        self.WIDTH = app.WIDTH
        self.HEIGHT = app.HEIGHT
        self.app = app
        self.x = 0
        self.y = 0
        self.surf = pygame.Surface((app.WIDTH, app.HEIGHT))
        self.background = None
        self.backgroundImage = None
        self.pics = []

        # animate
        self.activity_state = ACTIVITY_START
        self._animateIn = None
        self._animateOut = None
        if 'state' in self.app.activityData:
            if 'animateIn' in self.app.activityData['state']:
                self._animateIn = eval(self.app.activityData['state']['animateIn']['animate'])
                self._animateInStart = eval(self.app.activityData['state']['animateIn']['start'])
                self._animateInEnd = eval(self.app.activityData['state']['animateIn']['end'])
                self._animateInSpeed = 0.3
                if 'speed' in self.app.activityData['state']['animateIn']:
                    self._animateInSpeed = eval(self.app.activityData['state']['animateIn']['speed'])
            if 'animateOut' in self.app.activityData['state']:
                self._animateOut = eval(self.app.activityData['state']['animateOut']['animate'])
                self._animateOutStart = eval(self.app.activityData['state']['animateOut']['start'])
                self._animateOutEnd = eval(self.app.activityData['state']['animateOut']['end'])
                self._animateOutSpeed = 0.3
                if 'speed' in self.app.activityData['state']['animateOut']:
                    self._animateOutSpeed = eval(self.app.activityData['state']['animateOut']['speed'])

    def update(self):
        if self.activity_state == ACTIVITY_START:
            if self._animateIn:
                if self._animateIn(self,self._animateInStart,self._animateInEnd,self._animateInSpeed):
                    self.activity_state = ACTIVITY_RUN
            else:
                self.activity_state = ACTIVITY_RUN
        elif self.activity_state == ACTIVITY_CLOSE:
            if self._animateOut:
                if self._animateOut(self,self._animateOutStart,self._animateOutEnd,self._animateOutSpeed):
                    self.app.close()
            else:
                self.app.close()

        if self.background != None:
            if  isinstance(self.background,tuple):
                self.surf.fill(self.background)
                print('activity back')
            else:
                if self.backgroundImage == None:
                    self.backgroundImage = pygame.image.load(self.background).convert()
                    self.backgroundImage = pygame.transform.scale(self.backgroundImage,(self.WIDTH,self.HEIGHT))
                self.surf.blit(self.backgroundImage,(0,0))
        else:
            self.surf = pygame.Surface((self.WIDTH, self.HEIGHT))
            # self.surf.fill(BROWN)
    def close(self):
        self.activity_state = ACTIVITY_CLOSE

# key
    def onKeyDown(self, key, e):
        if self.activity_state == ACTIVITY_START or self.activity_state == ACTIVITY_CLOSE:
            return True
        return False

    def onKeyContinueDown(self, key, e):
        if self.activity_state == ACTIVITY_START or self.activity_state == ACTIVITY_CLOSE:
            return

    def onKeyUp(self, key, e):
        if self.activity_state == ACTIVITY_START or self.activity_state == ACTIVITY_CLOSE:
            return

# position
    def center(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int((self.app.HEIGHT-rect.bottom)/2)
        return (w,h)

    def position(self, rect, position):

        x = position[0]*1.0
        y = position[1]*1.0
        if position[0] == CENTER:
            # auto center
            w = int((self.app.WIDTH-rect.right)/2)
        else:
            w = int(self.app.WIDTH*x)
        if position[1] == CENTER:
            h = int((self.app.HEIGHT-rect.bottom)/2)
        else:
            h = int(self.app.HEIGHT*y)
        return (w,h)

    def picture(self, content, size, position):
        size = (int(size[0]*1.0*self.WIDTH),int(size[1]*1.0*self.HEIGHT))
        content = pygame.image.load(content).convert_alpha()
        content = pygame.transform.scale(content,size)
        self.surf.blit(content,self.position(content.get_rect(),position))

    def text(self, text='', size=FONT_NORMAL, position=(0,0), color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.app.scaleToHeightPixel(size)).render(text, True, color)
        rect = font.get_rect()
        self.surf.blit(font,self.position(rect,position))

    def textCenterTitle(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.app.scaleToHeightPixel(2.4)).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.2)
        self.surf.blit(font,(w,h))
    def textCenter1(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.app.scaleToHeightPixel(1.3)).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.45)
        self.surf.blit(font,(w,h))
    def textCenter2(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.app.scaleToHeightPixel(1.3)).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.6)
        self.surf.blit(font,(w,h))
    def textCenter3(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, self.app.scaleToHeightPixel(1.3)).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.75)
        self.surf.blit(font,(w,h))
