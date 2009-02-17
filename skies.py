import pygame
from pygame.locals import *
from game_clock import *
from globals import *



night_back = pygame.image.load('data/images/scenario/skies/night_back/night_back.png').convert_alpha()
night_front = pygame.image.load('data/images/scenario/skies/night_front/night_front.png').convert_alpha()

class Sky():
    def __init__(self, background,level):
        self.background = pygame.image.load(background).convert()
        self.count = 0
        self.count is (clock_pointer.count-120)
        for i in level:
            i.darkness.insert(0,night_back)
            i.darkness.insert(1,night_front)
            i.sky.insert(0,self)
    def set_light(self):
        if game_clock.time == ('morning' or 'day'):
           night_back.set_alpha(0)
           night_front.set_alpha(0)
        elif game_clock.time == 'night':
            night_back.set_alpha(self.count)
            night_front.set_alpha(self.count)
