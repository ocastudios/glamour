import pygame
import utils.obj_images as obj_images
from pygame.locals import *
from settings import *

class Billboard():
    def __init__(self,level):
        self.level = level
        self.image = obj_images.scale_image(pygame.image.load(data_dir+'/images/scenario/bathhouse_st/billboard_city/billboard/billboard_city.png').convert_alpha())
        self.size = self.image.get_size()[0]
        self.center_distance = ((self.size - self.level.universe.width)*self.level.universe.center_x)/(self.level.size-self.level.universe.width)
        self.pos = [self.center_distance, self.level.universe.floor - self.image.get_size()[1]]

    def update_all(self):
        self.pos[0] = ((self.size - self.level.universe.width)*self.level.universe.center_x)/(self.level.size -self.level.universe.width)


