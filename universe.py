import pygame
import game_clock
import stage
import os
from settings import *

class Universe():
    def __init__(self):
        default_resolution = (1440,900)
        w = int(default_resolution[0]*scale)
        h = int(default_resolution[1]*scale)
        print w
        print h
        self.main_dir = os.getcwd()
        self.center_x = int(-3400*scale)
        self.center_y = 0
        self.floor = self.height = h
        self.width = w
        self.speed = 0
        self.LEVEL = 'menu'
        self.action = [None,'stay']
        self.dir    = 0
        self.click = False
        self.screen_surface = pygame.display.set_mode((w,h),32)
        pygame.display.set_caption("Glamour - OcaStudios")
        self.level = stage.Stage(self)
        self.file = None
        self.frames_per_second = 20
        self.run_level = True


    def define_level(self):
        self.gclock =  game_clock.GameClock(self.level)
        self.clock_pointer = game_clock.ClockPointer(self.level)
        self.level.BathhouseSt()

    def movement(self,dir):
        max_speed = 10*scale
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed< -max_speed:
            self.speed = -max_speed
        self.center_x += self.speed
        if self.center_x > 0:
            self.speed = 0
            self.center_x = 0
        if self.center_x - self.width < -(self.level.size):
            self.speed = 0
            self.center_x = -(self.level.size) + self.width
