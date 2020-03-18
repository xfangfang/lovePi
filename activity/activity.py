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

    def title(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.2)
        return (w,h)
    def content1(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.5)
        return (w,h)
    def content2(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.6)
        return (w,h)
    def content3(self, rect):
        w = int((self.app.WIDTH-rect.right)/2)
        h = int(self.app.HEIGHT*0.7)
        return (w,h)
