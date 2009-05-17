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
        self.white = Foreground(self)

    def define_level(self):
        self.gclock =  game_clock.GameClock(self.level)
        self.clock_pointer = game_clock.ClockPointer(self.level)
        self.level.BathhouseSt()

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
class Foreground():
    def __init__(self,universe):
        self.pos = 0,0
        self.image = pygame.Surface((universe.width,universe.height)).convert()
        self.image.fill((255,255,255))
        self.alpha_value = 0
        self.inside = True
        self.image.set_alpha(self.alpha_value)
    def update_all(self):
        if self.inside:
            if self.alpha_value < 200:
                self.alpha_value += 5
        else:
            if self.alpha_value > 50:
                self.alpha_value -= 5
        self.image.set_alpha(self.alpha_value)

