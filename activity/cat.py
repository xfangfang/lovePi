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


class CatGame(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)
        self.state = CATGAME_INIT
        self.initBricks()

    def init(self):
        self.surf.fill(WHITE)
        self.textCenterTitle('加油！')
        self.textCenter1('帮助你的男人打败他')
        self.textCenter2('A 开始')
        self.textCenter3('B 暂停')

    def pause(self):
        self.surf.fill(WHITE)
        self.textCenterTitle('暂停')
        self.textCenter1('A 继续游戏')

    def start(self):
        self.ball_x_v = 4
        self.ball_y_v = 4
        # ball y direction
        if pygame.sprite.spritecollide(self.ball, self.group_player, False):
            if self.ball_y_direction == 1:
                self.ball.Y = self.HEIGHT - self.ball.rect.height - self.user.rect.height
            else:
                self.ball.Y = self.bot.rect.height
            self.ball_y_direction *= -1
        else:
            self.ball.Y += self.ball_y_v * self.ball_y_direction
            if self.ball_y_direction == 1 and self.ball.Y + self.ball.rect.height >= self.HEIGHT:
                    self.state = CATGAME_LOSE
            elif self.ball_y_direction == -1 and self.ball.Y <= 0:
                    self.state = CATGAME_WIN
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
        self.textCenterTitle('游戏结束')
        self.textCenter1('A 重新开始')
        self.textCenter2('B 认命了')

    def win(self):
        self.surf.fill(WHITE)
        self.textCenterTitle('你赢啦')
        self.textCenter1('A 返回')

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
        self.ball.position = (centerX ,centerY)

        self.group_player = pygame.sprite.Group()
        self.group_player.add(self.user)
        self.group_player.add(self.bot)
        self.group_ball = pygame.sprite.Group()
        self.group_ball.add(self.ball)

        self.ball_y_direction = random.choice([-1,1])
        self.ball_x_direction = random.choice([-1,1])

    def update(self):
        if self.state == CATGAME_INIT:
            self.init()
        elif self.state == CATGAME_PAUSE:
            self.pause()
        elif self.state == CATGAME_START:
            self.start()
            self.surf = pygame.transform.rotate(self.surf, -90)
        elif self.state == CATGAME_LOSE:
            self.over()
        elif self.state == CATGAME_WIN:
            self.win()


    def onKeyDown(self, key, e):
        if self.state == CATGAME_INIT:
            if e == key.btn_key1: self.state = CATGAME_START
        elif self.state == CATGAME_START:
            if e == key.btn_key2: self.state = CATGAME_PAUSE
        elif self.state == CATGAME_PAUSE:
            if e == key.btn_key1: self.state = CATGAME_START
        elif self.state == CATGAME_LOSE:
            if e == key.btn_key1:
                self.initBricks()
                self.state = CATGAME_START
            elif e == key.btn_key2:
                self.app.activityData['status'] = CATGAME_LOSE
                self.app.close()
        elif self.state == CATGAME_WIN:
            if e == key.btn_key1:
                self.app.activityData['status'] = CATGAME_WIN
                self.app.close()

    def onKeyContinueDown(self, key, e):
        if self.state == CATGAME_START:
            if e == key.btn_down:
                self.user.X += 4
                if self.user.X >= self.WIDTH - self.user.rect.width :
                    self.user.X = self.WIDTH - self.user.rect.width
            elif e == key.btn_up:
                self.user.X -= 4
                if self.user.X <= 0:
                    self.user.X = 0
