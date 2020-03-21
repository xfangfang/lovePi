from activity.activity import Activity
from activity.cat import CatGame
from var import *
from utils import get_yaml_data
import yaml
import pygame


class MainActivity(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.background = WHITE
        self.gameloop = get_yaml_data(CONF_START)['gameloop']
        self.buildTag()
        self.gameState = 0
    def buildTag(self):
        self.tagMap = {}
        for i, state in enumerate(self.gameloop):
            if 'tag' in state:
                self.tagMap[state['tag']] = i
    def update(self):
        self.surf.fill(self.background)
        if self.gameState >= len(self.gameloop):
            self.gameState = 0
        state = self.gameloop[self.gameState]
        if state['type'] == 'text':
            if 'textCenterTitle' in state: self.textCenterTitle(state['textCenterTitle'])
            if 'textCenter1' in state: self.textCenter1(state['textCenter1'])
            if 'textCenter2' in state: self.textCenter2(state['textCenter2'])
            if 'textCenter3' in state: self.textCenter3(state['textCenter3'])
        elif state['type'] == 'activity':
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
