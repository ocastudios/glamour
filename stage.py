import pygame
from pygame.locals import *
from screen_surface import *
from globals import *

class Stage():
    def __init__(self,level,size,universe):
        self.level = level
        self.enemies = []
        self.scenarios = []
        self.background = []
        self.objects = []
        self.moving_scenario = []
        self.menus = []
        self.princesses = []
        self.clock = []
        self.floor_image = []
        self.darkness = []
        self.sky = []
        self.clouds = []
        self.size = size
        self.panel = []
        self.floor = universe.floor-186
        
        
        
    def blit_all(self,surface,act,dir):

        for i in self.sky:
            surface.blit(i.background,(0,0))
            i.set_light()
        #self.darkness[0].set_alpha(255)
        #surface.blit(self.darkness[0],(0,0))
        for i in self.clouds:
            i.movement(dir,act)
            i.set_image()
            surface.blit(i.image,i.pos)
        for i in self.background:
            surface.blit(i.image,i.pos)
            i.update_image()
        for i in self.moving_scenario:
            surface.blit(i.image,i.pos)
            i.set_pos(act,dir)
        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.scenarios:
            i.update_pos()
            surface.blit(i.image,i.pos)
        for i in self.enemies:
            i.movement()
            #i.set_image()
            #i.set_pos()
            #i.look_around()
            surface.blit(i.image,i.pos)
        for i in self.objects:
            if i.alive == True:
                surface.blit(i.image,i.pos)
        for i in self.menus:
            surface.blit(i.image,i.pos)
        for i in self.princesses:
            for part in i.parts:
                surface.blit(part.image,part.pos)
            for effect in i.effects:
                surface.blit(effect[0],effect[1])


        for i in self.floor_image:
            i.update_pos()
            surface.blit(i.image,i.pos)

        for i in self.panel:
            surface.blit(i[0],i[1])
            
