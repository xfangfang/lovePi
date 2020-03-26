
import pygame
import math
from var import *

animate_start_time = None

# 线性移动
# start(0,0) 1为屏幕宽
def activityLinearMove(activity, start, end, speed=0.3):
    global animate_start_time
    endX = end[0]*1.0*activity.WIDTH
    endY = end[1]*1.0*activity.HEIGHT
    if animate_start_time:
        dY = endY-activity.y
        dX = endX-activity.x
        activity.y += dY*speed
        activity.x += dX*speed
        if math.fabs(dY) < 2:
            activity.y = endY
        if math.fabs(dX) < 2:
            activity.x = endX
        if math.fabs(dY) < 2 and math.fabs(dX) < 2:
            animate_start_time = None
            return True
    else:
        activity.x = start[0]*1.0*activity.WIDTH
        activity.y = start[1]*1.0*activity.HEIGHT
        animate_start_time = pygame.time.get_ticks()
    return False

def activitySmallToBig(activity):
    pass

def activityBigToSmall(activity):
    pass
