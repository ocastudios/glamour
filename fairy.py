
import pygame
import obj_images
from pygame.locals import *
import random

class Fairy():
    """This class defines the tip fairy, who helps the princess during the game."""

    directory = 'data/images/interface/fairy_tips'
    def __init__(self, pos, level,margin=[10,10,10,10],dirty=False):
        self.size = (10,10)
        self.level = level
        self.center_distance    = pos
        self.pos        =  (1200,700)
#(self.level.universe.center_x+self.center_distance,
#                           self.level.universe.floor - 186 -self.size[1])

        self.lists_of_images = {
                        'mouth_speak': obj_images.TwoSided(self.directory+'/fairy_speak/',margin),
                        'mouth_smile': obj_images.There_and_back_again(self.directory+'/fairy_smile/',margin),

                        'eyes_eyes': obj_images.There_and_back_again(self.directory+'/fairy_eyes/',margin),
                        'eyes_blink':obj_images.There_and_back_again(self.directory+'/fairy_blink/',margin),

                        'wings_wings': obj_images.TwoSided(self.directory+'/fairy_wings/',margin),
                        'wings_fly':   obj_images.TwoSided(self.directory+'/fairy_fly_wings/',margin),

                        'body_fly': obj_images.There_and_back_again(self.directory+'/fairy_fly/',margin),
                        'body_stand_right': obj_images.There_and_back_again(self.directory+'/fairy_stand_right/',margin),
                        'body_stand_left' : obj_images.There_and_back_again(self.directory+'/fairy_stand_left/',margin)
                    }

        self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
        self.parts = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]

        self.size = self.parts[1].get_size()
        self.image = pygame.Surface(self.size,SRCALPHA).convert_alpha()

    def update_all(self):
        for key,value in self.lists_of_images.items():
            value.update_number()

        self.parts = self.define_selfparts()
        self.image = self.update_image()



    def define_selfparts(self):
        return [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]

    def update_image(self):
        image = pygame.Surface(self.size,SRCALPHA).convert_alpha()
        for i in self.parts:
            if i != None:
                image.blit(i,(0,0))
        return image


