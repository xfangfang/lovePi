import pygame

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
