import pygame
from var import *
from activity.activity import Activity

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, size, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.position = [initial_position[0],initial_position[1]]
INIT = 0
START = 1

class CatGame(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.len = 40
        self.x = 0
        self.y = 0
        self.surf = pygame.Surface((app.WIDTH, app.HEIGHT))
        self.state = INIT
        self.intStart()
        self.initBricks()
        self.update()

    def intStart(self):
        self.text1 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render('加油！', True, BLACK)
        self.text2 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render('帮助你的男人打败他', True, BLACK)
        rect = self.text1.get_rect()
        center = self.center(rect)
        self.surf.blit(self.text1, (center[0], center[1] - rect.bottom))
        center = self.center(self.text2.get_rect())
        self.surf.blit(self.text2, (center[0],center[1]+10))
        self.surf = pygame.transform.rotate(self.surf, -180)


    def initBricks(self):
        h = self.app.scaleToHeightPixel(1)
        w = self.app.scaleToWidthPixel(4)
        self.user = Brick(BLACK,(w,h),(self.WIDTH/2-w/2,self.HEIGHT-h))
        self.bot = Brick(BLACK,(w,h),(self.WIDTH/2-w/2,0))

    def update(self):
        if self.state == INIT:
            pass
        else:
            self.surf.fill(WHITE)
            self.surf.blit(self.user.surf, self.user.position)
            self.surf.blit(self.bot.surf, self.bot.position)
            self.surf = pygame.transform.rotate(self.surf, -180)
    def onKeyDown(self, key, e):
        if e == key.btn_key1:
            self.state = START
    def onKeyContinueDown(self, key, e):
        if e == key.btn_right:
            if self.user.position[0] + self.user.size[0] < self.WIDTH:
                self.user.position[0] += 4
            else:
                self.user.position[0] = self.WIDTH - self.user.size[0]
        elif e == key.btn_left:
            if self.user.position[0] > 0:
                self.user.position[0] -= 4
            else:
                self.user.position[0] = 0
