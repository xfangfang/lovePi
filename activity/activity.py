import pygame
from var import *

class Activity():
    def __init__(self, app):
        self.WIDTH = app.WIDTH
        self.HEIGHT = app.HEIGHT
        self.app = app
        self.x = 0
        self.y = 0
        self.surf = pygame.Surface((app.WIDTH, app.HEIGHT))

    def update(self):
        pass

    def onKeyDown(self, key, e):
        pass

    def onKeyContinueDown(self, key, e):
        pass

    def onKeyUp(self, key, e):
        pass

    def center(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int((self.app.HEIGHT-rect.bottom)/2)
        return (w,h)

    def textCenterTitle(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.2)
        self.surf.blit(font,(w,h))
    def textCenter1(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.5)
        self.surf.blit(font,(w,h))
    def textCenter2(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.6)
        self.surf.blit(font,(w,h))
    def textCenter3(self, text, color=BLACK):
        font = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render(text, True, color)
        rect = font.get_rect()
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.7)
        self.surf.blit(font,(w,h))
