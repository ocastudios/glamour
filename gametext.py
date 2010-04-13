import pygame
import os
from settings import *

class Horizontal():
    def __init__(self,text,pos,frame,fonte='Domestic_Manners.ttf', font_size=20, color=(0,0,0),second_font = 'Chopin_Script.ttf'):
        self.frame      = frame
        try:
            self.frame_position = self.frame.position
        except:
            self.frame_position = 0,0
        self.font      = pygame.font.Font('data/fonts/'+fonte,font_size*scale)
        self.image      = self.font.render(text,1,color)
        self.position   = pos
        self.size       = self.image.get_size()
        self.pos        = [self.frame_position[0]+                            self.position[0]-(self.size[0]/2),
                           self.frame_position[1]+                            self.position[1]-(self.size[1]/2)]

    def update_all(self):
        self.pos        = [self.frame_position[0]+self.position[0]-(self.size[0]/2),
                           self.frame_position[1]+self.position[1]-(self.size[1]/2)]


class Vertical(Horizontal):
    def __init__(self,text,pos,menu, fonte='Domestic_Manners.ttf',font_size = 30, color = (0,0,0)):
        Horizontal.__init__(self,text,pos,menu,fonte,font_size,color)
        self.image = pygame.transform.rotate(self.image,90)


