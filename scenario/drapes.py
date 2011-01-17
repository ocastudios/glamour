import utils.obj_images as obj_images
import pygame
import os
import random
from settings import *
import settings.getscreen as getscreen

def p(positions):
    return [int(round(i*scale)) for i in positions ]
class Drape():
    images= getscreen.prep_images
    def __init__(self):
        size = p((1440,900))
        directory = main_dir+'/data/images/interface/omni/drapes/drapes/'
        frames = []
        drapes_size = p([720,900])
        speed  = 0
        right_x     = 0
        left_x      = 645*scale
        del getscreen.prep_images
        self.image = self.images[0]
        self.action = 'stay'
        self.speed = 0
        self.image_number = 0
        self.size = self.image.get_size()
        self.counter = 0


    def update_all(self):
        self.counter += 1
        if self.counter >5:
            if self.action == "open" and self.image_number < len(self.images)-1:
                self.image_number +=1
            elif self.action =="close" and self.image_number > -len(self.images):
                self.image_number -=1
            self.image = self.images[self.image_number]


class UperDrape():
    def __init__(self):
#        size = (1540,356)
#        prep = pygame.Surface(size, pygame.SRCALPHA)
#        tile = pygame.image.load(main_dir+'/data/images/interface/omni/drapes/upper_drapes/0.png').convert_alpha()
#        x = 0
#        for i in range(14):
#            prep.blit(tile,(x,0))
#            x += 110
#        pygame.image.save(prep, main_dir+'/data/images/interface/omni/drapes/upper_drapes/upper.png')
        self.image = obj_images.image(main_dir+'/data/images/interface/omni/drapes/upper_drapes/upper.png')
        self.action = 'stay'
        self.y = 0
        self.size_y = 356*scale

    def update_all(self):
        if self.action == 'open':
            self.y -= (3*scale)
        if self.y < -self.size_y:
            self.y = -self.size_y
