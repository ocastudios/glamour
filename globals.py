
import pygame
from pygame.locals import *
import pygame.display
import os
from getscreen import os_screen
from stage import *
from globals import *
from game_clock import *





class Universe():
    def __init__(self):
        self.gravity = 3
        self.center_x = 0
        self.center_y = 0
        self.floor = os_screen.current_h
        self.speed = 0
    def movement(self,dir):
        max_speed = 11
        if self.speed > max_speed:
            self.speed = max_speed
        elif self.speed< -max_speed:
            self.speed = -max_speed
        self.center_x += self.speed
        if self.center_x > 0:
            self.speed = 0
            self.center_x = 0
        if self.center_x < -5000:
            self.speed = 0
            self.center_x = -5000
#        self.center_x += self.speed


#Create lists

data_list = []
clouds = []
cenario_stuff = []
action = [None, 'stand']
stars = []
bunnies = []
enemies = []
clock = pygame.time.Clock()


dir = None
count = 0

universe = Universe()

Level_01 = Stage(1,2000,universe)
game_clock = GameClock([Level_01])
clock_pointer = ClockPointer([Level_01])



