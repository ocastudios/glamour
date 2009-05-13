import pygame
import game_clock
import stage

class Universe():
    def __init__(self,w,h):
        self.gravity = 3
        self.center_x = -3400
        self.center_y = 0
        self.floor = self.height = h
        self.width = w
        self.speed = 0
        self.LEVEL = 'menu'
        self.mouse_pos  = pygame.mouse.get_pos()
        self.action = [None,'stay']
        self.dir    = 0
        self.click = False
        self.screen_surface = pygame.display.set_mode((w,h),pygame.FULLSCREEN,32)
        self.level = stage.Stage(6000,self)

    def define_level(self):
        self.gclock =  game_clock.GameClock(self.level)
        self.clock_pointer = game_clock.ClockPointer(self.level)
        if self.LEVEL == 'bathhouse_st':
            self.level.BathhouseSt()
        if self.LEVEL == 'dress_st':
            self.level.DressSt()
        if self.LEVEL == 'accessory_st':
            self.level.AccessorySt()


    def movement(self,dir):

        max_speed = 10
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed< -max_speed:
            self.speed = -max_speed
        self.center_x += self.speed
        if self.center_x > 0:
            self.speed = 0
            self.center_x = 0
        if self.center_x < -(self.level.size-470):
            self.speed = 0
            self.center_x = -(self.level.size-470)
#        self.center_x += self.speed
