import obj_images
import pygame
import os
from settings import *


class Drape():
    images = None
    def __init__(self,position_x,side):
        directory = 'data/images/interface/omni/drapes/drapes/'
        if side == 'right':
            self.side = ('right','left')
        else:
            self.side = ('left','right')
        frames_list = sorted(os.listdir(directory))
        frames = []
        drapes_size = [800,900]
        for i in frames_list:
            image = pygame.Surface(drapes_size, pygame.SRCALPHA).convert_alpha()
            tile = pygame.image.load(directory+i).convert_alpha()
            tile_size = tile.get_size()
            for x in range(0,drapes_size[0]+tile_size[0],110):
                image.blit(tile,(x,0))
            frames += [image]
        frames_right = [pygame.transform.flip(img,1,0) for img in frames]
        self.images_left =  [obj_images.scale_image(i) for i in frames]
        self.images_right = [obj_images.scale_image(i) for i in frames_right]
        self.action = 'stay'
        self.speed = 0
        self.image_number = 0
        if self.side[0] == 'left':
            self.image = self.images_left[0]
        else:
            self.image = self.images_right[0]
        self.size = self.image.get_size()
        self.position = (position_x,0)
        self.counter = .2

    def update_all(self):
        if self.side[0]== 'left':
            order = ('open','close')
        else:
            order = ('close','open')
        if self.action == order[0]:
            if self.speed <  15*scale:
                self.speed += 2*scale
        elif self.action == order[1]:
            if self.speed > -15*scale:
                self.speed -= 2*scale
        else:
            self.speed = 0
        self.position = (self.position[0]+self.speed,0)
        if self.speed != 0:
            exec('self.image = self.images_'+self.side[0]+'[self.image_number]')
            if self.image_number + self.counter < len(self.images_left)-1:
                if self.speed >= 0:
                    self.image_number = int(self.image_number + self.counter)
                else:
                    self.image_number = -int(self.image_number + self.counter)
                self.counter += .1
            else:
                self.image_number = len(self.images_left)-1


class UperDrape():
    def __init__(self):
        size = (1540,356)
        prep = pygame.Surface(size, pygame.SRCALPHA)
        tile = pygame.image.load('data/images/interface/omni/drapes/upper_drapes/0.png').convert_alpha()
        x = 0
        for i in range(14):
            prep.blit(tile,(x,0))
            x += 110
        self.image = obj_images.scale_image(prep)
        self.action = 'stay'
        self.position = [0,0]
        self.size = (1540*scale,356*scale)

    def update_all(self):
        if self.action == 'open':
            self.position[1] -= (3*scale)
        if self.position[1] < -self.size[1]:
            self.position[1] = -self.size[1]
