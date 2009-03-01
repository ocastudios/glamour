from getscreen import *
from pygame.locals import *
pygame.mixer.init()
import random
from sys import exit
from math import *
from random import randint
from stage import *
from game_clock import *
from obj_images import *
from numpy import uint8


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
        if self.center_x < -9000:
            self.speed = 0
            self.center_x = -9000
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



