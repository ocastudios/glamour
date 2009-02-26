import pygame
from pygame.locals import *
from screen_surface import *
from globals import *

class Stage():
    """This class is meant to create the levels of the game. One of its most importante features is to blit everything on the screen and define what should be in each of the stages.
It is still in its early development"""
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
        self.cameras = []
        self.pointer = []
        self.floor = universe.floor-186
        self.floor_heights = {}
        self.set_floor()
        #self.floor_list = {0:186,620:186}
        

    def what_is_my_height(self,object):
        try:        y_height = self.floor_heights[object.distance_from_center]
        except:     y_height = 186
        return      y_height

    def blit_all(self,surface,act,dir,universe):
        for i in self.cameras:
            i.update_pos(universe,self.princesses[0])
        universe.movement(dir)

        for i in self.sky:
            surface.blit(i.background,(0,0))
            i.set_light()

        for i in self.clouds:
            surface.blit(i.image,i.pos)
            i.movement(dir,act)
            i.set_image()

        for i in self.background:
            surface.blit(i.image,i.pos)
            i.update_image()
        for i in self.moving_scenario:
            surface.blit(i.image,i.pos)
            i.set_pos(act,dir)

        for i in self.scenarios:
            surface.blit(i.image,i.pos)
            i.update_pos()

        for i in self.enemies:
            surface.blit(i.image,i.pos)
            i.movement((self.princesses[0]))

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
            i.update_pos(act,dir)
        for i in self.floor_image:
            surface.blit(i.image,i.pos)
            i.update_pos()

        for i in self.clock:
            surface.blit(i.image,i.pos)
        for i in self.panel:
            surface.blit(i[0],i[1])
        for i in self.pointer:
            surface.blit(i.image,i.pos)

    def set_floor(self):
        self.floor_heights = {}
        count = 0
        n = 1070
        a = 10
        while count < 1200:
            self.floor_heights[n+count] = 186
            if count >= 260 and count <= 299:
                self.floor_heights[n+count] = 186 + a
            if count >= 290 and count <= 329:
                self.floor_heights[n+count] = 196 + a
            if count >= 320 and count <= 359:
                self.floor_heights[n+count] = 206 + a
            if count >= 350 and count <= 399:
                self.floor_heights[n+count] = 216 + a
            if count >= 390 and count <= 439:
                self.floor_heights[n+count] = 236 + a
            if count >= 430 and count <= 499:
                self.floor_heights[n+count] = 246 + a
            if count >= 490 and count <= 729:
                self.floor_heights[n+count] = 256 + a
            if count >= 730 and count <= 789:
                self.floor_heights[n+count] = 246 + a
            if count >= 790 and count <= 839:                self.floor_heights[n+count] = 236 + a
            if count >= 840 and count <= 879:                self.floor_heights[n+count] = 226 + a
            if count >= 880 and count <= 899:                self.floor_heights[n+count] = 216 + a
            if count >= 910 and count <= 939:                self.floor_heights[n+count] = 206 + a
            if count >= 940 and count <= 969:                self.floor_heights[n+count] = 196 + a

            count += 1
        print self.floor_heights
