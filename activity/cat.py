import pygame
import random
from var import *
from activity.activity import Activity

class Brick(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
    def X():
        doc = "The X property."
        def fget(self):
            return self.rect.x
        def fset(self, value):
            self.rect.x = value
        return locals()
    def Y():
        doc = "The Y property."
        def fget(self):
            return self.rect.y
        def fset(self, value):
            self.rect.y = value
        return locals()
    def position():
        doc = "The position property."
        def fget(self):
            return self.rect.topleft
        def fset(self, value):
            self.rect.topleft = value
        return locals()
    X = property(**X())
    Y = property(**Y())
    position = property(**position())

INIT = 0
START = 1
PAUSE = 2
OVER = 3
WIN = 4

class CatGame(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.state = INIT
        self.initBricks()

    def init(self):
        self.surf.fill(WHITE)
        self.text1 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render('加油！', True, BLACK)
        self.text2 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render('帮助你的男人打败他', True, BLACK)
        rect = self.text1.get_rect()
        center = self.center(rect)
        self.surf.blit(self.text1, (center[0], center[1] - rect.bottom))
        center = self.center(self.text2.get_rect())
        self.surf.blit(self.text2, (center[0],center[1]+10))

    def pause(self):
        self.surf.fill(WHITE)
        self.text1 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render('暂停', True, BLACK)
        self.text2 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render('加油哦', True, BLACK)
        rect = self.text1.get_rect()
        center = self.center(rect)
        self.surf.blit(self.text1, (center[0], center[1] - rect.bottom))
        center = self.center(self.text2.get_rect())
        self.surf.blit(self.text2, (center[0],center[1]+10))

    def start(self):
        self.ball_x_v = 2
        self.ball_y_v = 2
        # ball y direction
        if pygame.sprite.spritecollide(self.ball, self.group_player, False):
            if self.ball_y_direction == 1:
                self.ball.Y = self.HEIGHT - self.ball.rect.height - self.user.rect.height
            else:
                self.ball.Y = self.bot.rect.height
            self.ball_y_direction *= -1
        else:
            self.ball.Y += self.ball_y_v * self.ball_y_direction
            if self.ball_y_direction == 1:
                if self.ball.Y + self.ball.rect.height >= self.HEIGHT:
                    self.state = OVER
            elif self.ball_y_direction == -1:
                if self.ball.Y <= 0:
                    self.state = WIN
                    # self.ball.Y = 0
                    # self.ball_y_direction = 1
        # ball x direction
        self.ball.X += self.ball_x_v * self.ball_x_direction
        if self.ball_x_direction == 1:
            if self.ball.X >= self.WIDTH - self.ball.rect.width:
                self.ball_x_direction = -1
                self.ball.X = self.WIDTH - self.ball.rect.width
        elif self.ball_x_direction == -1:
            if self.ball.X <= 0:
                self.ball.X = 0
                self.ball_x_direction = 1

        # bot move
        if self.ball_y_direction == -1:
            t = (self.ball.Y - self.bot.rect.height) / self.ball_y_v
            p_x = self.ball.X + t * self.ball_x_v * self.ball_x_direction
            if int(p_x / self.WIDTH)%2 == 0:
                p_x = p_x % self.WIDTH
            else:
                p_x = self.WIDTH - (p_x % self.WIDTH)
            if p_x > self.bot.X + 4 and p_x < self.bot.X + self.bot.rect.width - 4:
                pass
            else:
                if self.bot.X + self.bot.rect.width/2 < p_x:
                    self.bot.X += 3
                else:
                    self.bot.X -= 3
            if self.ball_x_direction == 1 and self.bot.X >= self.WIDTH - self.bot.rect.width :
                self.bot.X = self.WIDTH - self.bot.rect.width
            elif self.ball_x_direction == -1 and self.bot.X <= 0:
                self.bot.X = 0

        # update screen
        self.surf.fill(WHITE)
        self.group_player.draw(self.surf)
        self.group_ball.draw(self.surf)

    def over(self):
        self.surf.fill(WHITE)
        self.text1 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render('游戏结束', True, BLACK)
        self.text2 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render('A 重新开始', True, BLACK)
        rect = self.text1.get_rect()
        center = self.center(rect)
        self.surf.blit(self.text1, (center[0], center[1] - rect.bottom))
        center = self.center(self.text2.get_rect())
        self.surf.blit(self.text2, (center[0],center[1]+10))
    def win(self):
        self.surf.fill(WHITE)
        self.text1 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(2))+10).render('你赢啦', True, BLACK)
        self.text2 = pygame.font.Font(FONT_FILE_PATH, int(self.app.scaleToHeightPixel(1))+4).render('A 返回', True, BLACK)
        rect = self.text1.get_rect()
        center = self.center(rect)
        self.surf.blit(self.text1, (center[0], center[1] - rect.bottom))
        center = self.center(self.text2.get_rect())
        self.surf.blit(self.text2, (center[0],center[1]+10))
    def initBricks(self):
        self.brick_h = self.app.scaleToHeightPixel(1)
        self.brick_w = self.app.scaleToWidthPixel(4)
        size = (self.brick_w,self.brick_h)
        image = pygame.Surface(size)
        image.fill(BLACK)
        self.user = Brick(image)
        self.user.position = (self.WIDTH/2-self.brick_w/2,self.HEIGHT-self.brick_h)
        self.bot = Brick(image)
        self.bot.position = (self.WIDTH/2-self.brick_w/2,0)

        image = pygame.Surface((self.brick_h, self.brick_h))
        image.fill(RED)
        self.ball = Brick(image)
        centerY = self.center(self.ball.rect)[1]
        centerX = random.randint(int(self.WIDTH*0.1),int(self.WIDTH*0.9))
        print(centerX)
        self.ball.position = (centerX ,centerY)

        self.group_player = pygame.sprite.Group()
        self.group_player.add(self.user)
        self.group_player.add(self.bot)
        self.group_ball = pygame.sprite.Group()
        self.group_ball.add(self.ball)

        self.ball_y_direction = random.choice([-1,1])
        self.ball_x_direction = random.choice([-1,1])

    def update(self):
        if self.state == INIT:
            self.init()
        elif self.state == PAUSE:
            self.pause()
        elif self.state == START:
            self.start()
        elif self.state == OVER:
            self.over()
        elif self.state == WIN:
            self.win()

        self.surf = pygame.transform.rotate(self.surf, -90)

    def onKeyDown(self, key, e):
        if self.state == INIT:
            if e == key.btn_key1: self.state = START
        elif self.state == START:
            if e == key.btn_key2: self.state = PAUSE
        elif self.state == PAUSE:
            if e == key.btn_key2: self.state = START
        elif self.state == OVER:
            if e == key.btn_key1:
                self.initBricks()
                self.state = START
            elif e == key.btn_key2:
                pass
        elif self.state == WIN:
            if e == key.btn_key1:
                self.initBricks()
                self.state = START
            elif e == key.btn_key2:
                pass


    def onKeyContinueDown(self, key, e):
        if self.state == START:
            if e == key.btn_down:
                self.user.X += 4
                if self.user.X >= self.WIDTH - self.user.rect.width :
                    self.user.X = self.WIDTH - self.user.rect.width
            elif e == key.btn_up:
                self.user.X -= 4
                if self.user.X <= 0:
                    self.user.X = 0
