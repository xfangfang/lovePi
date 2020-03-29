import os
import pygame
from var import *
if ENV == PI:
    import RPi.GPIO as GPIO

class Key():
    def __init__(self):
        self.btn_up = 6
        self.btn_down = 19
        self.btn_left = 5
        self.btn_right = 26
        self.btn_key1 = 21
        self.btn_key2 = 20
        self.btn_key3 = 16
        self.btn_press = 13
        self.btn_list = [self.btn_up, self.btn_down, self.btn_left, self.btn_right, self.btn_key1, self.btn_key2, self.btn_key3, self.btn_press]
        self.env = ENV
        if ENV == PI:
            self.initGPIO()
        else:
            self.initKeyboard()
    def initKeyboard(self):
        self.key_list = [pygame.K_w, pygame.K_x, pygame.K_a, pygame.K_d, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_s, ]
        self.key_map = {}
        self.key_list_flag = {}
        for i in range(len(self.key_list)):
            self.key_map[self.key_list[i]] = self.btn_list[i]
        for i in self.key_list:
            self.key_list_flag[i] = False

    def initGPIO(self):

        GPIO.setmode(GPIO.BCM)
        self.btn_list_flag = {}

        for i in self.btn_list:
            self.btn_list_flag[i] = False
        for i in self.btn_list:
            GPIO.setup(i, GPIO.IN,GPIO.PUD_UP)

    def setOnKeyUpListener(self, listener):
        self.onKeyUpListener = listener

    def setOnKeyDownListener(self, listener):
        self.onKeyDownListener = listener

    def setOnKeyContinueDownListener(self, listener):
        self.onKeyContinueDownListener = listener

    def _setOnKeyContinueDown(self, key):
        if self.onKeyContinueDownListener:
            self.onKeyContinueDownListener(self, key)

    def _setOnKeyDown(self, key):
        if self.onKeyDownListener:
            self.onKeyDownListener(self, key)

    def _setOnKeyUp(self, key):
        if self.onKeyUpListener:
            self.onKeyUpListener(self, key)

    def update(self):
        if self.env == PI:
            for i in self.btn_list:
                if (not GPIO.input(i)): # button pressed
                    if not self.btn_list_flag[i]:
                        self._setOnKeyDown(i)
                    self._setOnKeyContinueDown(i)
                    self.btn_list_flag[i] = True
                if self.btn_list_flag[i] and GPIO.input(i): # button released
                    self.btn_list_flag[i] = False
                    self._setOnKeyUp(i)
        else:
            keys = pygame.key.get_pressed()
            for i in self.key_list:
                if keys[i]:
                    if not self.key_list_flag[i]:
                        self._setOnKeyDown(self.key_map[i])
                    self._setOnKeyContinueDown(self.key_map[i])
                    self.key_list_flag[i] = True
                if self.key_list_flag[i] and not keys[i]:
                    self._setOnKeyUp(self.key_map[i])
                    self.key_list_flag[i] = False
