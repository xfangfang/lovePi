from activity.activity import Activity
from activity.cat import CatGame
from var import *
from animate import *
from utils import get_yaml_data
import threading
import yaml
import pygame
import math
import os
import datetime
import random


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

class StartActivity(Text):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.state = START
        self.conf = None
        self.start()

        self.stopShow = True
        self.stopThread = False
        self.image_thread()
        self.time_thread()

    def start(self):
        self.pics = [self.getPicture(BACKGROUND_WM,(1,1),(0,0))]
        self.texts = [self.getText(text='LOVE is YOU', size=FONT_TITLE, position=(CENTER,0.15), color=WHITE)]
        if os.path.exists(USERLOG):
            with open(USERLOG,'r') as f:
                res = f.read().split(',')
                if len(res) == 2:
                    self.conf = res[0]
                    self.gameState = int(res[1])
                    self.texts.append(self.getText(text='A 继续游戏', size=FONT_NORMAL, position=(CENTER,0.45)))
                    self.texts.append(self.getText(text='B 重新开始', size=FONT_NORMAL, position=(CENTER,0.55)))
                    self.texts.append(self.getText(text='C 　其他　', size=FONT_NORMAL, position=(CENTER,0.65)))
                    return
        self.texts.append(self.getText(text='A 开始游戏', size=FONT_NORMAL, position=(CENTER,0.5)))
        self.texts.append(self.getText(text='B 　其他　', size=FONT_NORMAL, position=(CENTER,0.6)))

    def setting(self):
        self.pics = [self.getPicture(BACKGROUND_WM,(1,1),(0,0))]
        self.texts = [self.getText(text='其他', size=FONT_TITLE, position=(CENTER,0.15), color=WHITE)]
        self.texts.append(self.getText(text='A 回忆时钟', size=FONT_NORMAL, position=(CENTER,0.45)))
        self.texts.append(self.getText(text='B 软件更新', size=FONT_NORMAL, position=(CENTER,0.55)))
        self.texts.append(self.getText(text='C 　关于　', size=FONT_NORMAL, position=(CENTER,0.65)))
        self.texts.append(self.getText(text='按下"方向键"返回主页', size=FONT_SMALL, position=(0,0), color=GREY))


    def image_thread(self):
        if not self.stopShow:
            self.app.background = self.images[self.imageNum]
            self.imageNum += 1
            self.imageNum %= len(self.images)
            pic = self.images[self.imageNum]
            self.pics = [BLACK,self.getPicture(pic,(1,1),(0,0))]
        if not self.stopThread:
            t = threading.Timer(5, self.image_thread)
            t.start()

    def time_thread(self):
        if not self.stopShow:
            if self.activity_state != ANIMATE_START:
                self.time = datetime.datetime.now().strftime('%H:%M:%S')
                self.texts = [self.getText(self.time, size=FONT_LARGE, position=(0.05,CENTER),color=WHITE)]
        if not self.stopThread:
            t = threading.Timer(1, self.time_thread)
            t.start()

    def close(self):
        Activity.close(self)
        self.stopThread = True

    def onKeyDown(self, key, e):
        if Activity.onKeyDown(self, key, e): return
        if self.state == START:
            self.app.background = (138, 163, 161)
            if self.conf != None:
                if e == key.btn_key1:
                    self.app.switchConfig(self.conf, self.gameState)
                    self.close()
                elif e == key.btn_key2:
                    self.state = SHOW_TIP_NEWGAME
                    self.pics.append(self.getPicture(PIC_SPEEK_P_LEFT,(1,1),(0,0)))
                    self.texts = [self.getText('开始新游戏', FONT_NORMAL, (CENTER,LINE_4), BLACK)]
                    self.texts.append(self.getText('将清空之前的游戏记录', FONT_NORMAL, (CENTER,LINE_3), BLACK))
                    self.texts.append(self.getText('A 新游戏   B 取消', FONT_NORMAL, (CENTER,LINE_1), BLACK))
                elif e == key.btn_key3:
                    self.state = SETTING
                    self.setting()
                    self.activity_state = ANIMATE_START
                    self.app.background = self.surf.copy()
                    self.setAnimateIn(animate=activityLinearMove, start=(1,0), end=(0,0))
            else:
                if e == key.btn_key1:
                    self.close()
                elif e == key.btn_key2:
                    self.state = SETTING
                    self.setting()
                    self.activity_state = ANIMATE_START
                    self.app.background = self.surf.copy()
                    self.setAnimateIn(animate=activityLinearMove, start=(1,0), end=(0,0))
        elif self.state == SETTING:
            if e == key.btn_key1:
                images = os.listdir(IMAGES_ROOT)
                self.images = []
                for i in images:
                    self.images.append(IMAGES_ROOT+'/'+i)
                random.shuffle(self.images)
                self.imageNum = 0
                self.stopShow = False
                self.time = datetime.datetime.now().strftime('%H:%M:%S')
                self.texts = [self.getText(self.time, size=FONT_LARGE, position=(0.05,CENTER),color=WHITE)]
                self.pics = [BLACK,self.getPicture(self.images[0],(1,1),(0,0))]
                self.state = IMAGES
            elif e == key.btn_key2:
                self.state = UPDATE
                self.pics.append(self.getPicture(PIC_SPEEK_P_LEFT,(1,1),(0,0.2)))
                self.texts = [self.getText('按任意键开始检查更新', FONT_NORMAL, (CENTER,LINE_2), BLACK)]
            elif e == key.btn_key3:
                self.pics = [(249, 231, 238)]
                self.texts = [self.getText('送给小陈', FONT_NORMAL, (CENTER,CENTER), BLACK)]
                self.state = RETURN_SETTING
            elif e == key.btn_press:
                self.state = START
                self.start()
                self.activity_state = ANIMATE_START
                self.app.background = self.surf.copy()
                self.setAnimateIn(animate=activityLinearMove, start=(-1,0), end=(0,0))

        elif self.state == SHOW_TIP_NEWGAME:
            if e == key.btn_key1:
                self.close()
            elif e == key.btn_key2:
                self.state = START
                self.start()
        elif self.state == UPDATE:
            try:
                res = os.popen('git pull').readlines()
                if res[0] == 'Already up to date.\n':
                    self.state = RETURN_SETTING
                    self.texts = [self.getText('已经是最新的版本了', FONT_NORMAL, (CENTER,LINE_2), BLACK)]
                else:
                    self.state = SHOW_TIP_REBOOT
                    self.texts = [self.getText('检查到新版本 按任意键重启', FONT_NORMAL, (CENTER,LINE_2), BLACK)]
                    self.stopThread = True
            except Exception as e:
                self.state = RETURN_SETTING
                self.pics = [self.getPicture(PIC_QRCODE,(1,1),(0,0))]
                self.texts = []
        elif self.state == RETURN_SETTING:
            self.state = SETTING
            self.setting()
        elif self.state == SHOW_TIP_REBOOT:
            os.system('sudo reboot now')
        elif self.state == IMAGES:
            self.stopShow= True
            self.app.background = BROWN
            self.state = SETTING
            self.setting()

class Choice(Text):
    def onKeyDown(self, key, e):
        if Activity.onKeyDown(self, key, e): return
        if e == key.btn_key1:
            self.app.activityData['status'] = CHOICE_YES
            self.close()
        elif e == key.btn_key2:
            self.app.activityData['status'] = CHOICE_NO
            self.close()

class TanTan(Text):
    def __init__(self, app):
        Text.__init__(self, app)
        self.state = TAN_START
        self.men = [PIC_TAN_JING, PIC_TAN_XIAN, PIC_TAN_FANG, PIC_TAN_CHANG]
        self.config = [CONF_TAN_JING, CONF_TAN_XIAN, CONF_TAN_FANG, CONF_TAN_CHANG]
        self.selectNum = 0
        self.state = TAN_START
        self.start()

    def start(self):
        self.pics = [TANTAN_BACKGROUND, self.getPicture(PIC_TANTAN,(0.3,0.3),(CENTER,0.2))]
        self.texts = [self.getText('左右滑动，揭晓缘分', FONT_NORMAL, (CENTER,LINE_2), WHITE)]

    def seek(self):
        self.app.background = TANTAN_BACKGROUND
        man = self.men[self.selectNum]
        self.pics = [TANTAN_BACKGROUND, self.getPicture(man,(1,1),(CENTER,CENTER))]
        self.pics.append(self.getPicture(PIC_TANTAN,(0.1,0.1),(0.02,0.02)))
        self.pics.append(self.getPicture(ICON_HEART,(0.15,0.15),(CENTER,0.7)))
        self.pics.append(self.getPicture(ICON_ARROW_LEFT,(0.15,0.15),(0.05,CENTER)))
        self.pics.append(self.getPicture(ICON_ARROW_RIGHT,(0.15,0.15),(0.8,CENTER)))
        self.texts = [self.getText('A 心动', FONT_NORMAL, (CENTER,LINE_1), RED)]

    def confirm(self):
        pass

    def onKeyDown(self, key, e):
        if Activity.onKeyDown(self, key, e): return
        if self.state == TAN_START:
            if e == key.btn_left:
                self.state = TAN_SEEK
                self.seek()
                self.activity_state = ANIMATE_START
                self.setAnimateIn(animate=activityLinearMove, start=(1,0), end=(0,0))
            elif e == key.btn_right:
                self.state = TAN_SEEK
                self.seek()
                self.activity_state = ANIMATE_START
                self.setAnimateIn(animate=activityLinearMove, start=(-1,0), end=(0,0))
        elif self.state == TAN_SEEK:
            if e == key.btn_key1:
                self.state = TAN_CONFIRM
                self.pics.append(self.getPicture(PIC_SPEEK_P_LEFT,(1,1),(0,0.2)))
                self.texts = [self.getText('你确定选择他吗？', FONT_NORMAL, (CENTER,LINE_2), BLACK)]
                self.texts.append(self.getText('A 确定    B 再看看', FONT_NORMAL, (CENTER,LINE_1), BLACK))
            elif e == key.btn_left:
                self.app.background = self.men[self.selectNum]
                self.selectNum -= 1
                self.selectNum = self.selectNum % len(self.men)
                man = self.men[self.selectNum]
                self.pics[1] = self.getPicture(man,(1,1),(CENTER,CENTER))
                self.activity_state = ANIMATE_START
                self.setAnimateIn(animate=activityLinearMove, start=(1,0), end=(0,0))
            elif e == key.btn_right:
                self.app.background = self.men[self.selectNum]
                self.selectNum += 1
                self.selectNum = self.selectNum % len(self.men)
                man = self.men[self.selectNum]
                self.pics[1] = self.getPicture(man,(1,1),(CENTER,CENTER))
                self.activity_state = ANIMATE_START
                self.setAnimateIn(animate=activityLinearMove, start=(-1,0), end=(0,0))

        elif self.state == TAN_CONFIRM:
            if e == key.btn_key1:
                # choose game yaml
                conf = self.config[self.selectNum]
                self.app.switchConfig(conf, 0)
                self.close()
            elif e == key.btn_key2:
                self.pics.pop()
                self.seek()
                self.state = TAN_SEEK
