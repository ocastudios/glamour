import obj_images
import pygame
from pygame.locals import *

class Sky():
    def __init__(self, background,level,clock_pointer):
        directory = 'data/images/scenario/skies/'
        self.background = pygame.image.load(background).convert()
        self.count = 0
        self.count = (clock_pointer.count-120)
        self.night_back = obj_images.OneSided(directory+'night_back/')
        self.night_front = obj_images.OneSided(directory+'night_front/')
        self.image_number = 0
        self.max_image_number = len(self.night_back.list)-1
    def update_all(self):
        pass
