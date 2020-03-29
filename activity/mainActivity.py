from activity.activity import Activity
from activity.cat import CatGame
from var import *
from utils import get_yaml_data
import yaml
import pygame
import math


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

class StartActivity(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.background = BACKGROUND_WM
    def update(self):
        super().update()
        self.text(text='LOVE IS YOU', size=FONT_TITLE, position=(CENTER,0.15))
        self.text(text='A 开始游戏', size=FONT_NORMAL, position=(CENTER,0.55))
        self.text(text='B 检查更新', size=FONT_NORMAL, position=(CENTER,0.7))
    def onKeyDown(self, key, e):
        if super().onKeyDown(key, e): return
        if e == key.btn_key1:
            self.close()
        elif e == key.btn_key2:
            self.app.updateAndRestart()

class Text(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        # self.cat = MySprite(self.surf)
        # self.cat.load("assets/test.png", 100, 100, 4)
        # self.group = pygame.sprite.Group()
        # self.group.add(self.cat)
        # self.cat.position = (100,100,100,100)
        self.pics = []
        self.texts = []
        state = self.app.activityData['state']
        if 'pics' in state:
            for pic in state['pics']:
                content = eval(pic['content'])
                if isinstance(content,tuple):
                    self.pics.append(content)
                else:
                    position = eval(pic['position'])
                    size = eval(pic['size'])
                    self.pics.append(self.getPicture(content, size, position))
        if 'texts' in state:
            for text in state['texts']:
                color = BLACK
                size = FONT_NORMAL
                if 'color' in text : color = eval(text['color'])
                if 'size' in text : size = eval(text['size'])
                t = self.getText(text=text['content'], size=size, position=eval(text['position']), color=color)
                self.texts.append(t)

    def update(self):
        super().update()
        state = self.app.activityData['state']
        for i in self.pics:
            if len(i) == 2:
                self.surf.blit(*i)
            else:
                self.surf.fill(i)
        for i in self.texts:
            self.surf.blit(*i)

        # # ticks = pygame.time.get_ticks()
        # self.group.update(ticks)
        # self.group.draw(self.surf)



    def onKeyDown(self, key, e):
        if super().onKeyDown(key, e): return
        if e == key.btn_key1:
            self.close()

class Choice(Text):
    def onKeyDown(self, key, e):
        Activity.onKeyDown(self, key, e)
        if e == key.btn_key1:
            self.app.activityData['status'] = CHOICE_YES
            self.close()
        elif e == key.btn_key2:
            self.app.activityData['status'] = CHOICE_NO
            self.close()

class TanTan(Activity):
    pass
