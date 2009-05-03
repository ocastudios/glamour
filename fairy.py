
import pygame
import obj_images
from pygame.locals import *
import random

class Fairy():
    """This class defines the tip fairy, who helps the princess during the game."""

    directory = 'data/images/interface/fairy_tips'
    def __init__(self,speed,directory, pos, level,margin=[10,10,10,10],dirty=False):
        self.center_distance    = pos
        self.pos        = (self.level.universe.center_x+self.center_distance,
                           self.level.universe.floor - 186 -self.size[1])

        self.mouth = {'speak': obj_images.There_and_back_again(self.directory+'/fairy_speak/',margin),
                      'smile': obj_images.There_and_back_again(self.directory+'/fairy_smile/',margin)}

        self.eyes  = {'eyes': obj_images.There_and_back_again(self.directory+'/fairy_eyes/',margin),
                      'blink':obj_images.There_and_back_again(self.directory+'/fairy_blink/',margin)}


        self.wings = {'wings': obj_images.There_and_back_again(self.directory+'fairy_wings/',margin),
                      'fly':   obj_images.There_and_back_again(self.directory+'fairy_fly_wings/',margin)}

        self.body  = {'fly': obj_images.There_and_back_again(self.directory+'fairy_fly',margin),
                      'stand_right': obj_images.There_and_back_again(self.directory+'fairy_stand_right',margin),
                      'stand_left' : obj_images.There_and_back_again(self.directory+'fairy_stand_left',margin)}


        self.speed      = 10

