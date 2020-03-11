import os
import pygame

PI = 1
PC = 2

class Key():
    def __init__(self):
        self.btn_up = 5
        self.btn_down = 26
        self.btn_left = 19
        self.btn_right = 6
        self.btn_key1 = 21
        self.btn_key2 = 20
        self.btn_list = [self.btn_up, self.btn_down, self.btn_left, self.btn_right, self.btn_key1, self.btn_key2]

        if "GAME_DEV" in os.environ and os.environ["GAME_DEV"] == 'PI':
            self.dev = PI
            self.initGPIO()
        else:
            self.dev = PC
            self.initKeyboard()
    def initKeyboard(self):
        self.key_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_u, pygame.K_i]
        self.key_map = {}
        self.key_list_flag = {}
        for i in range(len(self.key_list)):
            self.key_map[self.key_list[i]] = self.btn_list[i]
        for i in self.key_list:
            self.key_list_flag[i] = False

    def initGPIO(self):
        import RPi.GPIO as GPIO
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

    def _setOnKeyDown(self, key):
        self.onKeyDownListener(self, key)

    def _setOnKeyUp(self, key):
        self.onKeyUpListener(self, key)

    def update(self):
        if self.dev == PI:
            for i in self.btn_list:
                if (not GPIO.input(i)): # button pressed
                    if not self.btn_list_flag[i]:
                        self._setOnKeyDown(i)
                    self.btn_list_flag[i] = True
                if self.btn_list_flag[i] and GPIO.input(i): # button released
                    self.btn_list_flag[i] = False
                    self._setOnKeyUp(i)
        else:
            keys = pygame.key.get_pressed()
            for i in self.key_list:
                if not self.key_list_flag[i] and keys[i]:
                    self._setOnKeyDown(self.key_map[i])
                    self.key_list_flag[i] = True
                if self.key_list_flag[i] and not keys[i]:
                    self._setOnKeyUp(self.key_map[i])
                    self.key_list_flag[i] = False
