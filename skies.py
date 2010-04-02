import obj_images
import pygame
import os
from pygame.locals import *

class Sky():
    def __init__(self, background,level,clock_pointer):
        directory = 'data/images/scenario/skies/'
        self.level = level
        self.image = pygame.image.load(background).convert()
        self.count = (clock_pointer.count-120)
        self.pos = (0,0)
        self.night_images = obj_images.OneSided('data/images/scenario/skies/night2/')
        self.night_image = None
        self.prev = None

    def update_all(self):
        if self.level.universe.clock_pointer.time == 'evening' or self.level.universe.clock_pointer.time == 'night':
            self.night_image = self.night_images.list[self.night_images.number]
            if self.level.universe.clock_pointer.count%2== 0 and self.level.universe.clock_pointer.count != self.prev:
                self.night_images.til_the_end()
                self.prev = self.level.universe.clock_pointer.count
        else:
            self.night_image = None


