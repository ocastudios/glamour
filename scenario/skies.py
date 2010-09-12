import utils.obj_images as obj_images
import pygame
import os
from pygame.locals import *

class Sky():
    night_images = obj_images.OneSided('data/images/scenario/skies/night2/')
    def __init__(self,level):
        self.level = level
        self.image = obj_images.image('data/images/scenario/skies/daytime/daytime.png')
        self.pos = (0,0)
        self.night_image = None
        self.prev = None

    def update_all(self):
        if self.level.clock[1].time in ('evening', 'night'):
            self.night_image = self.night_images.list[self.night_images.number]
            if self.level.clock[1].count%2== 0 and self.level.clock[1].count != self.prev:
                self.night_images.til_the_end()
                self.prev = self.level.clock[1].count
        else:
            self.night_image = None
            self.night_images.number = 0
