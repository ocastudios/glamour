
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
        self.universe = self.level.universe
        self.center_distance    = pos
        self.pos        =  [600,700]
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
        self.goalpos = [1200,700]
        self.direction= "left"

    def update_all(self):
        for key,value in self.lists_of_images.items():
            value.update_number()
        if self.direction == "left":
            self.parts = [self.lists_of_images[i].left[self.lists_of_images[i].number] for i in self.images_strings]
        else:
            self.parts = [self.lists_of_images[i].right[self.lists_of_images[i].number] for i in self.images_strings]
        self.image = self.update_image()


        if self.pos != self.goalpos:
            self.fly_to_goal()
        else:
            if self.pos[0]>(self.universe.width/2):
                self.direction = "left"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
            else:
                self.direction = "right"
                self.images_strings = ['wings_wings','body_stand_left','mouth_speak','eyes_eyes']
    def update_image(self):
        image = pygame.Surface(self.size,SRCALPHA).convert_alpha()
        for i in self.parts:
            if i:
                image.blit(i,(0,0))
        return image

    def fly_to_goal(self):
        speed = 10
        self.images_strings = ["wings_fly","body_fly"]
        if self.pos[0]>self.goalpos[0]:
            self.direction = "left"
            self.pos[0] -= speed
        elif self.pos[0]<self.goalpos[0]:
            self.direction = "right"
            self.pos[0] += speed
        if self.pos[1]>self.goalpos[1]:
            self.pos[1] -= speed
        elif self.pos[1]<self.goalpos[1]:
            self.pos[1] += speed
