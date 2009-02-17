
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
    def movement(self,dir,pace):
        if dir == 'right':
            self.center_x -= pace
        if dir == 'left':
            self.center_x += pace
            
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



