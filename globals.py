from getscreen import *
from pygame.locals import *
pygame.mixer.init()
import random
from sys import exit
from math import *
from random import randint
from stage import *
from game_clock import *
import obj_images
from numpy import uint8


class Universe():
    def __init__(self):
        self.gravity = 3
        self.center_x = -3400
        self.center_y = 0
        self.floor = os_screen.current_h
        self.width = os_screen.current_w
        self.speed = 0
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
        if self.center_x < -5430:
            self.speed = 0
            self.center_x = -5430
#        self.center_x += self.speed


#Create lists

action = [None, 'stay']
clock = pygame.time.Clock()

dir = None
count = 0
universe = Universe()






