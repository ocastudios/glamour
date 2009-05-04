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
        self.level = 'menu'
        self.mouse_pos  = pygame.mouse.get_pos()
        self.action = [None,'stay']
        self.dir    = 0
        self.click = False

    def define_level(self):
        if self.level == 'bathhouse_st':
            self.actual_level = stage.BathhouseSt(1,6000,self,'bathhouse_st/')
        if self.level == 'dress_st':
            self.actual_level = stage.DressSt(1,6000,self,'dress_st/')
        if self.level == 'accessory_st':
            self.actual_level = stage.AccessorySt(1,10000,self,'accessory_st/')
        self.gclock =  game_clock.GameClock(self.actual_level)
        self.clock_pointer = game_clock.ClockPointer(self.actual_level)

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
        if self.center_x < -(self.actual_level.size-470):
            self.speed = 0
            self.center_x = -(self.actual_level.size-470)
#        self.center_x += self.speed
