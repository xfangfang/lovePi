from activity.activity import Activity
from activity.cat import CatGame
from var import *
from utils import get_yaml_data
import yaml
import pygame
import math


class MainActivity(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.gameloop = get_yaml_data(CONF_START)['gameloop']
        self.buildTag()
        self.gameState = 0
    def buildTag(self):
        self.tagMap = {}
        for i, state in enumerate(self.gameloop):
            if 'tag' in state:
                self.tagMap[state['tag']] = i
    def update(self):
        if self.gameState >= len(self.gameloop):
            self.gameState = 0
        state = self.gameloop[self.gameState]
        if 'appBackground' in state:
            self.app.background = eval(state['appBackground'])
        if state['type'] == 'activity':
            self.app.activityData['state'] = state
            self.app.openActivity(eval(state['activity']))
            self.gameState += 1
        elif state['type'] == 'goto':
            if 'status' in self.app.activityData:
                if self.app.activityData['status'] == eval(state['if']):
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

    def onKeyDown(self, key, e):
        if e == key.btn_key2:
            if self.background == WHITE:
                self.background = RED
            else:
                self.background = WHITE
        elif e == key.btn_key1:
            self.gameState += 1

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
    def position():
        doc = "The position property."
        def fget(self):
            return self.rect
        def fset(self, value):
            self.rect = value
        return locals()
    position = property(**position())

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 0,0,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=FPS):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


class Text(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        # self.cat = MySprite(self.surf)
        # self.cat.load("assets/test.png", 100, 100, 4)
        # self.group = pygame.sprite.Group()
        # self.group.add(self.cat)
        # self.cat.position = (100,100,100,100)
        self.state = ACTIVITY_START

    def update(self):
        super().update()
        state = self.app.activityData['state']
        if 'background' in state: self.background =  eval(state['background'])
        if 'textCenterTitle' in state: self.text(text=state['textCenterTitle'], size=FONT_TITLE, position=(-1,0.15))
        if 'textCenter1' in state: self.text(text=state['textCenter1'], size=FONT_NORMAL, position=(-1,0.45))
        if 'textCenter2' in state: self.textCenter2(state['textCenter2'])
        if 'textCenter3' in state: self.textCenter3(state['textCenter3'])
        if 'texts' in state:
            for text in state['texts']:
                color = BLACK
                size = FONT_NORMAL
                if 'color' in text : color = eval(text['color'])
                if 'size' in text : size = eval(text['size'])
                self.text(text=text['content'], size=size, position=eval(text['position']), color=color)
        # ticks = pygame.time.get_ticks()
        # self.group.update(ticks)
        # self.group.draw(self.surf)



    def onKeyDown(self, key, e):
        if super().onKeyDown(key, e): return
        if e == key.btn_key1:
            self.close()



class Choice(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
    def update(self):
        self.surf.fill(WHITE)
        state = self.app.activityData['state']
        if 'textCenterTitle' in state: self.textCenterTitle(state['textCenterTitle'])
        if 'textCenter1' in state: self.textCenter1(state['textCenter1'])
        if 'textCenter2' in state: self.textCenter2(state['textCenter2'])
        if 'textCenter3' in state: self.textCenter3(state['textCenter3'])
    def onKeyDown(self, key, e):
        if e == key.btn_key1:
            self.app.activityData['status'] = CHOICE_YES
            self.app.close()
        elif e == key.btn_key2:
            self.app.activityData['status'] = CHOICE_NO
            self.app.close()
