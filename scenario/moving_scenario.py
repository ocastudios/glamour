import pygame
import utils
import settings
from settings import directory
import os

class Billboard():
    def __init__(self,level):
        self.level = level
        self.image = utils.img.image(os.path.join(directory.scenario,'bathhouse_st','billboard_city','billboard','billboard_city.png'))
        self.size = self.image.get_size()[0]
        self.center_distance = ((self.size - self.level.universe.width)*self.level.universe.center_x)/(self.level.size-self.level.universe.width)
        self.pos = [self.center_distance, self.level.universe.floor - self.image.get_size()[1]]

    def update_all(self):
        self.pos[0] = ((self.size - self.level.universe.width)*self.level.universe.center_x)/(self.level.size -self.level.universe.width)
