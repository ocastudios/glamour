from globals import *
from obj_images import *
import random
from random import randint
from getscreen import os_screen

class Bunny():
    walk = None
    def __init__(self,pos):
        self.life = 1000
        self.size = (150,100)
        self.pos = (((os_screen.current_w*20)/100),Level_01.floor-self.size[1])
        self.rect = Rect(self.pos,self.size)
        if self.walk == None:
            self.walk = ObjectImages('data/images/bunny/')
        self.image_number = 0
        self.move = False
        self.dir = 'left'
        self.distance_from_center = pos
        self.speed = 6
        self.pos = (self.distance_from_center[0], 200)
        self.count = 0
        bunnies.append(self)

    def set_pos(self):
       
        self.pos = (universe.center_x+self.distance_from_center[0], Level_01.floor-self.size[1])
        actual_list = self.walk.left
        if self.dir == 'right' :
            self.distance_from_center = (self.distance_from_center[0]+self.speed,self.distance_from_center[1])
            actual_list = self.walk.right
        else:
            self.distance_from_center = (self.distance_from_center[0]-self.speed,self.distance_from_center[1])
            actual_list = self.walk.left
        
        number_of_files = len(actual_list)-2

        if self.image_number <= number_of_files:
            self.image_number +=1
        else:
            self.image_number = 0

        self.image = actual_list[self.image_number]

        self.size = self.image.get_size()

